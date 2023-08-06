# Setup Teardown Content Decorator

This is a simple package that aims to make adding setup and teardown to pytest flavored tests quick and painless.

# Installation
```
python3 -m pip install setup-teardown
```

# Decorator Usage

## Custom Database Class
```
from setup_teardown import SetupTeardown

class PgSetupTeardown(SetupTeardown):
    def setup(self):
        # Perform test setup
        self.session = db.session.new_session()
        self.session.query(self.table).delete()
        return self

    def teardown(self, typ, val, traceback):
        # Perform test teardown
        self.session.query(self.table).delete()
```

## Example test with decorator usage
```
class TestHandlerDatabaseRequired:
    @PgSetupTeardown(table="table_name")
    def test_handler_success(self, mock_datetime):
        """
        Example of using the SetupTeardown ContextDecorator with arbitrary setup and teardown
        """
        assert 1 == 1
        # Effect the database test that may leave db in dirty state
```

## Example test with context manager usage

```
    def setup(self):
        db.session.new_session().query(self.table).delete()

    def teardown(self):
        db.session.new_session().query(self.table).delete()


    # context manager application example
    with PgSetupTeardown(setup=setup, teardown=teardown):
        assert 1 == 1
        # Effect the database test that may leave db in dirty state
```
