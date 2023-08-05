from omnitools import file_size, randstr, p, encodeURIComponent, def_template
from sfx7z.utils import FILTER_COPY, new_multi_volume_fo, lzma_filter
from requests_toolbelt.streaming_iterator import StreamingIterator
from .utils import glob_fns, glob_fns_size
from py7zr import SevenZipFile
from hashlib import sha256
import threadwrapper
import traceback
import threading
import requests
import zipfile
import shutil
import json
import time
import os
import re


class UCEFCUploader:
    pending_path = "pending"
    completed_path = "completed"
    failed_path = "failed"
    ready_path = "ready"
    skipped_path = "skipped"
    compilation_path = "compilation"
    zipped_path = "zipped"
    small_size = 8*1024*1024
    split_size = 4*1023*1023*1023
    from ucefc.pkg_data.pages.root import upload_page
    max_size = upload_page.max_size

    def __init__(self, domain, credentials):
        os.makedirs(self.pending_path, exist_ok=True)
        os.makedirs(self.completed_path, exist_ok=True)
        os.makedirs(self.failed_path, exist_ok=True)
        os.makedirs(self.ready_path, exist_ok=True)
        os.makedirs(self.skipped_path, exist_ok=True)
        self.domain = domain
        self.api_base = self.domain + "/api"
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "Chrome/96.0.13.59232"})
        self.s.post(self.api_base, {"op": "login", "username": credentials[0], "password": credentials[1]})
        self.root_folder = self.s.post(self.api_base, {"op": "get_folders"}).json()[0]
        self.compilation = {
            "display_name": "",
            "drive": "",
            "root": "",
            "relative_path": "",
            "files": []
        }

    def __del__(self):
        self.s.get(self.domain + "/logout")

    def get_file_generator(self, path, hash):
        def generator():
            nonlocal hash
            fo = open(path, "rb")
            while True:
                buffer = fo.read(65535)
                if not buffer:
                    break
                hash.update(buffer)
                yield buffer
            fo.close()

        return StreamingIterator(file_size(path), generator()), "application/octet-stream"

    def upload_worker(self, *args, **kwargs):
        r = self.s.post(*args, **kwargs)
        if r.status_code == 200:
            return r.status_code, r.json()
        else:
            return r.status_code, r.content.decode()

    def check_progress(self, fp, filesize, session, result):
        try:
            r = self.s.post(self.api_base, {"op": "get_server_progress", "session": session}, timeout=3)
            if r.status_code == 200:
                p("\r\t\t", fp, filesize, "progress", str(r.json()).zfill(3) + "%", end="")
            elif r.status_code >= 500:
                result.append([500, ConnectionError()])
                return
        except:
            pass

    def start_job(self, job, result):
        def _job():
            try:
                result.append(job())
            except:
                result.append([400, traceback.format_exc()])

        t = threading.Thread(target=_job)
        t.daemon = True
        t.start()

    @staticmethod
    def fp_to_upload_fp(fp):
        return re.sub(r"^([A-Za-z]\:\\|[A-Za-z]\:$)", r"\\", fp).replace(os.path.sep, "/")

    def split_file(self, fp, size):
        p("\r\t\t", fp, size, "splitting files", end="")
        mv_fo = new_multi_volume_fo(fp, volume=self.split_size, ext_digits=3)
        sz_fo = SevenZipFile(mv_fo, "w", filters=[lzma_filter(id=FILTER_COPY)])
        def job():
            nonlocal sz_fo
            nonlocal mv_fo
            try:
                sz_fo.write(fp, os.path.basename(fp))
                sz_fo.close()
                mv_fo.close()
            except Exception as e:
                try:
                    for _fp in glob_fns(fp):
                        if os.path.isfile(_fp):
                            os.unlink(_fp)
                except:
                    pass
                return e
        result = []
        self.start_job(def_template(job), result)
        while not result:
            p("\r\t\t", fp, size, "splitting files", "{:.2f}%".format(glob_fns_size(fp)/size*100), end="")
            time.sleep(1)
        if not result[0]:
            return glob_fns(fp)
        else:
            raise result[0]

    def upload_file(self, root, file):
        fp = file[0]
        abs_path = self.fp_to_upload_fp(fp)
        abs_path = os.path.dirname(abs_path)
        r_fp = self.fp_to_upload_fp(fp.replace(root, "")[1:])
        session = randstr(32)
        query = "?session={}&folder={}&path={}".format(
            session,
            self.root_folder,
            encodeURIComponent(abs_path),
        )
        filename = encodeURIComponent(os.path.basename(fp))
        p("\t\t", r_fp, "uploading", end="")
        filesize = file_size(fp)
        hash = sha256()
        if 0 < filesize < self.max_size:
            data, ctype = self.get_file_generator(fp, hash)
            result = []
            url = self.api_base+"/{}{}".format(filename, query)
            self.start_job(def_template(self.upload_worker, url, data=data, headers={"Content-Type": ctype}), result)
            while not result:
                self.check_progress(r_fp, filesize, session, result)
                time.sleep(1)
        elif filesize >= self.max_size:
            fns = []
            try:
                fns = self.split_file(fp, filesize)
                for _fp in list(fns):
                    self.upload_file(root, [_fp])
                    os.unlink(_fp)
                    fns.pop(0)
            except Exception as e:
                traceback.print_exc()
                raise StopIteration(e)
            finally:
                for _fp in fns:
                    try:
                        if os.path.isfile(_fp):
                            os.unlink(_fp)
                    except:
                        pass
            return
        else:
            result = [[406, "Invalid File Size"]]
        if result[0][0] == 200:
            try:
                link = self.domain+"/"+result[0][1]["id"]
            except Exception as e:
                p(result)
                raise e
            if result[0][1]["hash"] == hash.hexdigest():
                p("\r\t\t", r_fp, link)
                self.compilation["files"].append([r_fp, link])
            else:
                p("\r\t\t", r_fp, "different hash", error=True)
                self.s.post(self.api_base, {"op": "remove_file", "id": result[0][1]["id"]})
                self.compilation["files"].append([r_fp, ""])
        else:
            p("\r\t\t", r_fp, result[0][1], error=True)
            self.compilation["files"].append([r_fp, ""])
            if 400 <= result[0][0] < 500:
                raise ConnectionError
            else:
                raise StopIteration

    def upload_files(self, display_name, relative_path, root, files):
        fn = "{}.json".format(relative_path.replace("/", "___"))
        pending_fp = os.path.join(self.pending_path, fn)
        if os.path.isfile(pending_fp):
            self.compilation = json.loads(open(pending_fp, "rb").read().decode())
            self.compilation["files"] = [_ for _ in self.compilation["files"] if _[1]]
        else:
            self.compilation["display_name"] = display_name
            self.compilation["root"] = self.fp_to_upload_fp(root)
            self.compilation["relative_path"] = relative_path
            drive = re.search(r"^([A-Za-z]\:\\|[A-Za-z]\:$)", root)
            if drive:
                drive = drive[1]
                self.compilation["drive"] = drive.strip("\\")
        tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**2))
        for i, file in enumerate(list(files)):
            def job(file):
                self.upload_file(root, file)
                files.pop(0)
                if files:
                    open("queue.json", "wb").write(json.dumps(files).encode())
                open(pending_fp, "wb").write(json.dumps(self.compilation, indent=4).encode())
            job = def_template(job, file)
            if file_size(file[0]) <= self.small_size:
                tw.add(job=job)
            else:
                job()
        tw.wait()
        if not files:
            os.remove("queue.json")
        if not self.compilation["files"]:
            p("\t", "empty compilation", relative_path, error=True)
        elif not self.compilation["display_name"] or not all(_[1] for _ in self.compilation["files"]):
            p("\t", "manual compilation", relative_path, error=True)
        else:
            p("\t", "generating compilation", self.compilation["display_name"], end="")
            r = self.generate_compilation(self.compilation)
            if r[0] == 200:
                shutil.move(pending_fp, os.path.join(self.completed_path, fn))
                p("\r\t", "generated compilation", relative_path, self.compilation["display_name"], self.domain+"/"+r[1]["id"])
            else:
                p("\r\t", "manual compilation", relative_path, error=True)

    def upload(
            self, display_name, relative_path, root, filter,
            upload_small_first: bool = False,
            upload_large_first: bool = False
    ):
        p(root)
        root = root.rstrip("/").rstrip("\\")
        relative_path = self.fp_to_upload_fp(relative_path).strip("/")
        skipped = []
        files = []
        sizes = []
        size = 0
        path = os.path.sep.join([root, relative_path])
        if os.path.isfile("queue.json"):
            _files = json.loads(open("queue.json", "rb").read().decode())
            for file in _files:
                if filter(file[0]):
                    skipped.append(file[0])
                else:
                    files.append(file)
                    sizes.append(file_size(file[0]))
                    size += sizes[-1]/1024/1024/1024
                p("\r\t", file[0], end="")
        else:
            for a, b, c in os.walk(path):
                b.sort()
                c.sort()
                for d in c:
                    e = os.path.join(a, d)
                    if filter(e):
                        skipped.append(e)
                    else:
                        files.append([e])
                        sizes.append(file_size(e))
                        size += sizes[-1]/1024/1024/1024
                    p("\r\t", e, end="")
            if files:
                open("queue.json", "wb").write(json.dumps(files).encode())
        if skipped:
            skipped.insert(0, path)
            skipped.insert(1, "")
            open(os.path.join(self.skipped_path, "skipped_{}.txt".format(relative_path.replace("/", "___"))), "wb").write("\n".join(skipped).encode())
        if upload_small_first:
            files = [__ for _, __ in sorted(zip(sizes, files))]
        elif upload_large_first:
            files = [__ for _, __ in sorted(zip(sizes, files), reverse=True)]
        else:
            files = sorted(files, key=lambda x: x[0].split(os.path.sep))
        p("\r\t", relative_path, len(files), size)
        self.upload_files(display_name, relative_path, root, files)

    def generate_compilation(self, compilation):
        filename = compilation["display_name"] + ".zip"
        relative_path = compilation["relative_path"]
        _root = compilation["root"]
        drive = compilation["drive"]
        root_files = []
        for a, b, c in os.walk(os.path.join((drive+_root).replace("/", os.path.sep), relative_path)):
            for d in c:
                e = os.path.join(a, d)
                root_files.append(e.replace(os.path.sep, "/"))
        zip_fp = os.path.join(self.zipped_path, _root.strip("/"), relative_path, filename)
        os.makedirs(os.path.dirname(zip_fp), exist_ok=True)
        zip_fo = zipfile.ZipFile(zip_fp, "w")
        for file in compilation["files"]:
            fp = file[0].lstrip("/") + ".txt"
            _fp = os.path.join(self.compilation_path, _root.strip("/"), fp)
            if not any(_.endswith(file[0]) for _ in root_files):
                if os.path.isfile(_fp):
                    os.remove(_fp)
                    continue
            os.makedirs(os.path.dirname(_fp), exist_ok=True)
            open(_fp, "wb").write(file[1].encode())
            zip_fo.writestr(fp, file[1].encode())
        h2d = b"http://code.foxe6.kozow.com/ucefc/test/"
        h2dn = "how_to_download.txt"
        open(os.path.join(self.compilation_path, _root.strip("/"), h2dn), "wb").write(h2d)
        zip_fo.writestr(h2dn, h2d)
        zip_fo.close()
        session = randstr(32)
        query = "?session={}&folder={}&path={}".format(
            session,
            self.root_folder,
            encodeURIComponent(self.fp_to_upload_fp(os.path.join(_root, relative_path))),
        )
        data, ctype = self.get_file_generator(zip_fp, sha256())
        url = self.api_base + "/{}{}".format(filename, query)
        r = self.upload_worker(url, data=data, headers={"Content-Type": ctype})
        return r

    def generate_ready_compilation(self):
        for fn in os.listdir(self.ready_path):
            fp = os.path.join(self.ready_path, fn)
            compilation = json.loads(open(fp, "rb").read().decode())
            p("\t", "generating compilation", compilation["display_name"], end="")
            r = self.generate_compilation(compilation)
            if r[0] == 200:
                shutil.move(fp, os.path.join(self.completed_path, fn))
                p("\r\t", "generated compilation", compilation["display_name"], self.domain+"/"+r[1]["id"])
            else:
                shutil.move(fp, os.path.join(self.failed_path, fn))
                p("\r\t", "manual compilation", compilation["relative_path"], error=True)






