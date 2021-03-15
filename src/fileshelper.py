import os
import pathlib
from pathlib import Path
from shutil import copyfile

class FilesHelper:

    def __init__(self):
        pass

    def create_directory(self, path):
        if(os.path.isdir(path) ==False):
            try:
                return os.mkdir(path)
            except OSError:
                return False
        else:
            return True

    def create_file(self, content, path):
        confirm_path = Path(path).parent
        self.create_directory(confirm_path)
            
        f = open(path, "a")
        f.write(content)
        f.close()
        return True

    def backup_file(self, sourcepath, destinationpath):
        backup_file_name = os.path.basename(sourcepath)
        self.create_directory(destinationpath)
        result = copyfile(sourcepath, destinationpath + "\\" + backup_file_name)

        return result