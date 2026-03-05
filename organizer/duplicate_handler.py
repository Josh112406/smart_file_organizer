import os
import hashlib

class DuplicateHandler:
    def __init__(self):
        self.hash_store = {}
        self.duplicate_count = 0
        
    def generate_hash(self, file, algorithm: str = 'sha256') -> str:
        with open(file, 'rb') as f:
            digest = hashlib.file_digest(f, algorithm)
        return digest.hexdigest()
    
    def is_duplicate(self, file_path):
        file_path = os.path.abspath(file_path)
        file_hash = self.generate_hash(file_path)
        
        if file_hash in self.hash_store:
            self.duplicate_count += 1
            return True
        
        self.hash_store[file_hash] = file_path
        return False
    