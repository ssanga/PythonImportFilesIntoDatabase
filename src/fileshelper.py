import os
import pathlib
from pathlib import Path
from shutil import copyfile
import glob

class FilesHelper:

    def __init__(self):
        pass
    
    def get_file_name_without_extension(self, path):
        name = Path(path).stem
        name = name.replace('-','_')
        return name

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

    def move_file_to_backups(self, filename, file_prefix=None):
        path = os.getcwd()  
        path = path + '\\Backups\\'

        if not os.path.exists(path):
            os.mkdir(path)
    
        originalFileName = os.path.basename(filename)

        if(file_prefix != None):
            originalFileName = file_prefix + "_" + os.path.basename(filename)

        path = path + originalFileName

        os.replace(filename, path)
    
    def get_newest_file(self, path):
        list_of_files = glob.glob(path + '*.csv') # * means all if need specific format then *.csv

        if(list_of_files is True):
            latest_file = max(list_of_files, key=os.path.getctime)
            return latest_file
        else:
            return False

    def get_all_files(self, path):
        list_of_files = glob.glob(path + '*.csv') # * means all if need specific format then *.csv
        return list_of_files

    def delete_files(self, path):
        files = glob.glob(path + '*.csv')
        for f in files:
            os.remove(f)