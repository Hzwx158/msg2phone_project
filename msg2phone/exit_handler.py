import functools
import time
from abc import ABC, abstractmethod
import traceback

class ExitHandler(ABC):
    """Basic class for Exit Handler.
        For usage, you need to implement two methods: `on_success_exit` and `on_fail_exit`.
        You can use it as a content manager or decorator.
        See examples inside `_main` function in this file.
    """
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.on_success_exit()
        else:
            self.on_fail_exit(exc_type, exc_val, exc_tb)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                res = func(*args, **kwargs)
                return res
        return wrapper

    @abstractmethod
    def on_success_exit(self):
        pass
    @abstractmethod
    def on_fail_exit(self, exc_type, exc_value, exc_traceback):
        pass

    def format_error(self, exc_type, exc_value, exc_traceback):
        return ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))

def _main():
    class T(ExitHandler):
        def __init__(self, a):
            super().__init__()
            self.a = a    
        def on_success_exit(self):
            print(f"success {self.a}")
        def on_fail_exit(self, exc_type, exc_value, exc_traceback):
            print(f"fail {self.a}")
            with open("./tmp.txt", "w") as f:
                f.write(self.format_error(exc_type, exc_value, exc_traceback))

    with T(10):
        # print(10/0)
        print(10/5)
        for i in range(10000):
            time.sleep(1)


if __name__ == '__main__':
    _main()