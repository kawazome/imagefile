#!/user/local/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import piexif

class anyfile(object):

    def __init__(self,path):
        self._path = None
        self._name = None
        self._ext = None
        self._date = None
        if not anyfile.exist(path): return
        self._path = path
        self._name = os.path.basename(path)
        _, self._ext = os.path.splitext(path)
        self._date = anyfile.getdate(path)

    def clear(self):
        self._path = None
        self._name = None
        self._ext = None
        self._date = None

    def is_valid(self): return self._path != None

    def is_invalid(self): return self._path == None

    def path(self): return self._path

    def name(self): return self._name

    def ext(self): return self._ext

    def date(self): return self._date

    def date_isoformat(self): return self._date.isoformat()

    @classmethod
    def exist(cls,path):
        if path: return os.path.isfile(path)
        return False

    @classmethod
    def getdate(cls,path):
        if cls.exist(path): return datetime.fromtimestamp(os.stat(path).st_mtime)
        return None

class imagefile(anyfile):

    jpg_exts = ['.jpg', '.JPG']
    movie_exts = ['.mp4', '.MP4','.mov', '.MOV','.m4a', '.M4A','.m4v', '.M4V']
    exts = jpg_exts + movie_exts

    def __init__(self,path):
        self._image = None
        self._capture_date = None
        super().__init__(path)
        if not imagefile.check_ext(self._path): self.clear()

    def clear(self):
        super().clear()
        self._image = None
        self._capture_date = None

    def is_jpeg(self): return self.ext() in imagefile.jpg_exts

    def is_movie(self): return self.ext() in imagefile.movie_exts

    def open(self):
        if not self._path: return None
        if not self.is_jpeg(): return None
        self._image = imagefile.open_image(self._path)

    def width(self):
        if not self._image: self.open()
        if not self._image: return None
        w, h = self._image.size
        return w

    def height(self):
        if not self._image: self.open()
        if not self._image: return None
        w, h = self._image.size
        return h

    def getexif(self,fields):
        if not self._image: self.open()
        if not self._image: return None
        exif = self._image.getexif()
        dic = {}
        for key, value in exif.items():
            if TAGS.get(key) in fields: dic[TAGS.get(key, key)] = value
        return dic

    def caputure_date(self):
        if self._capture_date: return self._capture_date
        date = self.getexif("DateTimeOriginal")
        if not date: return None
        self._capture_date = datetime.strptime(date['DateTime'],'%Y:%m:%d %H:%M:%S')
        return self._capture_date

    def resize(self,save_dir, long_side=1000):
        if not self._image: self.open()
        if not self._image: return None
        if not os.path.isdir(save_dir): return None
        save_path = save_dir + '/' + self.name()
        exif = piexif.load(self._image.info["exif"])
        if self.width() < long_side and self.height() < long_side:
            shutil.copy2(self._path,save_path)
            return imagefile(save_path)
        img = self._image
        width = int(self.width() * long_side / max(self.width(),self.height()))
        height = int(self.height() * long_side / max(self.width(),self.height()))
        img = img.resize((width,height),Image.Resampling.LANCZOS)
        exif["0th"][piexif.ImageIFD.XResolution] = (width, 1)
        exif["0th"][piexif.ImageIFD.YResolution] = (height, 1)
        exif_bytes = piexif.dump(exif)
        img.save(save_path, "jpeg", exif=exif_bytes)
        return imagefile(save_path)

    @classmethod
    def check_ext(cls,path):
        _, ext = os.path.splitext(path)
        return ext in cls.exts

    @classmethod
    def open_image(cls, path):
        if not path: return None
        try: return Image.open(path)
        except OSError: return None

if __name__ == "__main__":
    img = imagefile("/Users/kawazome/Pictures/sample/dog/dog1.jpg")
    print("PATH:["+img.path()+"]")
    print("EXT:["+img.ext()+"]")
    print(img.caputure_date())
    print("WIDTH:["+str(img.width())+"]")
    print("HEIGHTT:["+str(img.height())+"]")

    small = img.resize("/Users/kawazome/Downloads",long_side=600)
    print("PATH:["+small.path()+"]")
    print("EXT:["+small.ext()+"]")
    print(small.caputure_date())
    print("WIDTH:["+str(small.width())+"]")
    print("HEIGHTT:["+str(small.height())+"]")


