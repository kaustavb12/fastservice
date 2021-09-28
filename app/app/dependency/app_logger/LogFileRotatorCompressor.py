from logging.handlers import RotatingFileHandler
import zlib
import os

# Rotates log file when size exceeds maxBytes and compresses old log files
class RotatorCompressorHandler(RotatingFileHandler):
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False) -> None:
        super().__init__(filename, mode=mode, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding, delay=delay)
        self.namer = self.rotate_file_name
        self.rotator = self.rotate_file_compress

    def rotate_file_name(self, name):
        return name + ".gz"

    def rotate_file_compress(self, source, dest):
        with open(source, "rb") as sf:
            data = sf.read()
            compressed = zlib.compress(data, 9)
            with open(dest, "wb") as df:
                df.write(compressed)
        os.remove(source)