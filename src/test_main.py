import main
from fileshelper import FilesHelper
import unittest
import os


class MainProgramTest(unittest.TestCase):
    
    def setUp(self):
        self.fileshelper = FilesHelper()
        
    # def test_initialise_log_file(self):
    #     self.working_path = os.path.dirname(os.path.abspath(__file__)) +  '\\TestDirectory\\'
    #     self.fileshelper.create_directory(self.working_path)
    #     main.initialise_log_file(self.working_path)
        
        
    def tearDown(self):
        self.fileshelper.delete_files(self.working_path)

    

       
    
         
    

