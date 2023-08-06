"""Setup Teardown helper classes."""
from functools import wraps


class ContextDecorator:
    """Setup Teardown base class."""

    def __init__(self, table: str, **kwargs):
        """Accept table name."""
        self.table = table
        self.__dict__.update(kwargs)

    def __enter__(self):
        return self

    def __exit__(self, typ, val, traceback):
        pass

    def __call__(self, _func):
        @wraps(_func)
        def wrapper(*args, **kw):
            with self:
                return _func(*args, **kw)

        return wrapper


class SetupTeardown(ContextDecorator):
    """Setup Teardown class."""

    def __enter__(self):
        self.setup(self)
        return self

    def __exit__(self, typ, val, traceback):
        self.teardown(self)

    def setup(self):
        print("setup")

    def teardown(self):
        print("teardown")
