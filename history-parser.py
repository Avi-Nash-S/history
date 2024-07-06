import uuid
import os
import time

class HistoryFileParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.execution_id = uuid.uuid4()
        self.reduction = ''
        self.write_path = f"history-snaps/{time.strftime('%Y%m%d_%H%M%S')}.logs"
        self.history = []

    def __enter__(self):
        print(f"Initializing {self.__class__.__name__}: {self.execution_id}")
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print(f"Exiting process: {self.execution_id}")
        return self

    def read(self):
        print(f"Reading file at {self.filepath}")
        with open(self.filepath, mode='r') as HistoryFile:
            out = HistoryFile.readlines()
            self.history = set(out)
            self.reduction = f"{len(out)} -> {len(self.history)}"
        return self
    
    def write(self, write_at = None):
        if write_at:
            self.write_path = write_at
        print(f"Creating history snapshot at: {self.write_path}")
        with open(self.write_path, mode='w+') as HistoryFileWrite:
            HistoryFileWrite.writelines(self.history)
        return self
    
    def delete(self, delete_at = None):
        delete_at = delete_at or self.filepath
        os.remove(delete_at)
        return self

    

if __name__ == "__main__":
    os.system("./create-history.zsh")
    filepath = os.getenv("FILEPATH")
    print(filepath)
    if filepath:
        with HistoryFileParser(filepath) as fileparser:
            fileparser.read()
            fileparser.write()
            fileparser.delete()
    else:
        raise Exception('File path not set.')

    

        


