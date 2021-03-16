from fileshelper import FilesHelper
import unittest
import os

# Control + Shift + P
# Python: Configure Tests
# https://code-maven.com/slides/python/pytest-class

class FilesHelperTest(unittest.TestCase):
    
    def setUp(self):
        self.fileshelper = FilesHelper()
        self.configure_folders_and_files()

    def configure_folders_and_files(self):
        content = 'created from test'
        self.working_path = os.path.dirname(os.path.abspath(__file__)) +  '\\TestDirectory\\'
        self.backup_directory = os.path.dirname(os.path.abspath(__file__)) + "\\backups"
        self.test_file = self.working_path + "01ISIN45678912test.csv"
        result = self.fileshelper.create_file(content, self.test_file)

        self.empty_folder = os.path.dirname(os.path.abspath(__file__)) +  '\\TestEmptyDirectory\\'
        self.fileshelper.create_directory(self.empty_folder)

    def tearDown(self):
        self.fileshelper.delete_files(self.working_path)

    def test_create_directory(self):
        result = self.fileshelper.create_directory(self.working_path)
        self.assertTrue(result)

    def test_backup_file(self):
         result = self.fileshelper.backup_file(self.test_file, self.backup_directory)
         self.assertTrue(result)

    def test_backup_file_error(self):
         self.assertRaises(FileNotFoundError,self.fileshelper.backup_file,'none','no_existe.txt')

    def test_get_newest_file_gets_new_file(self):
        result = self.fileshelper.get_newest_file(self.working_path)
        self.assertFalse(result)

    def test_get_newest_file_gets_None(self):
        result = self.fileshelper.get_newest_file(self.empty_folder)
        self.assertFalse(result)

    def test_get_all_files_gets_some_files(self):
        result = self.fileshelper.get_all_files(self.working_path)
        self.assertTrue(result)

    def test_get_all_files_gets_None(self):
        result = self.fileshelper.get_all_files(self.empty_folder)
        self.assertFalse(result)
         
    

