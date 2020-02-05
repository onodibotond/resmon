import unittest 
import monitor
import os

class TestStringMethods(unittest.TestCase): 
    
    self.test_path = '/tmp/test_resmon'
    self.test_file = '/tmp/test_resmon/test.tar.gz'

    def test_process_monitor(self): 
        self.assertBetween(monitor.get_ram_percent(), 0, 100) 
  
    def test_make_tarfile_exception(self):         
        self.assertRaises(monitor.make_tarfile("/inexistent/path/to/test/test.tar.gz", "/inexistent/path/to/test"), FileNotFoundError)
  
    def test_make_tarfile(self):
        os.mkdir(self.test_path)
        monitor.make_tarfile(self.test_file, self.test_path)
        self.assertTrue(os.path.exists(self.test_file))
        os.rmdir(self.test_path)
    
    def test_clean_old_files(self):
        os.mkdir(self.test_path)
        monitor.make_tarfile(self.test_file, self.test_path)
        monitor.clean_old_files(0, 0, self.test_file)
        self.assertTrue(os.path.exists(self.test_file))
        os.rmdir(self.test_path)
        
 
  
if __name__ == '__main__': 
    unittest.main() 