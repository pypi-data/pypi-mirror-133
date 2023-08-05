

import os 

class FileAccess:
    def change_directory(self, path: str):
        return os.chdir(path)
    def get_cloudpost_path(self):
        return os.path.dirname(os.path.dirname(__file__))

    def make_directory(self, name: str):
        return os.mkdir(name)

    def write_file(self, path: str, data: str):
        f = open(path, "w")
        f.write(data)
        f.close()

    def read_file(self, path: str):
        f = open(path)
        res = f.read()
        f.close()
        return res
    
    def list_directory(self, path: str):
        if path.endswith('__pycache__'):
            return []
        return os.listdir(path)
    
    def isfile(self, path):
        return os.path.isfile(path)
    
    def isdir(self, path):
        return os.path.isdir(path)