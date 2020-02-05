import unittest 
import monitor
import os

class TestStringMethods(unittest.TestCase): 
    
    def test_process_monitor(self): 
        self.assertTrue(0 >= monitor.get_ram_percent() and monitor.get_ram_percent() <= 100) 
  
    def test_make_tarfile_exception(self):         
        self.assertRaises(FileNotFoundError, monitor.make_tarfile("/inexistent/path/to/test/test.tar.gz", "/inexistent/path/to/test"))
  
    def test_make_tarfile(self):
        test_path = '/tmp/test_resmon'
        test_file = '/tmp/test_resmon/test.tar.gz'
        os.mkdir(test_path)
        monitor.make_tarfile(test_file, test_path)
        self.assertTrue(os.path.exists(test_file))
        os.rmdir(test_path)
    
    def test_clean_old_files(self):
        test_path = '/tmp/test_resmon'
        test_file = '/tmp/test_resmon/test.tar.gz'
        os.mkdir(test_path)
        monitor.make_tarfile(test_file, test_path)
        monitor.clean_old_files(0, 0, test_path)
        self.assertFalse(os.path.exists(test_file))
        os.rmdir(test_path)
        
  
if __name__ == '__main__': 
    unittest.main() 