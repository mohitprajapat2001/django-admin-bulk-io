from multiprocessing import Pool, Manager
from dataclasses import dataclass
from typing import Any


@dataclass
class MultiProcessPool:
    data: dict
    serializer: Any
    error_queue = None

    def validate_serialization(self, item):
        serializer = self.serializer(data=item)
        if serializer.is_valid():
            serializer.save()
        else:
            self.error_queue.put(serializer.errors)

    def multiprocess_pool(self):
        with Manager() as manager:
            self.error_queue = manager.Queue()
            with Pool(processes=4) as pool:
                pool.map(self.validate_serialization, self.data)
            errors = []
            while not self.error_queue.empty():
                errors.append(self.error_queue.get())
            return errors
