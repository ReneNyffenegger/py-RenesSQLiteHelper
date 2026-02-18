# RenesSQLiteHelper

René's minimal wrapper around Python's built-in `sqlite3` module.

## Installation

```bash
pip install RenesSQLiteHelper
```

## Usage

### Create a database

Note the first parameter (`__file__`) to create the database in a
filesystem path relative to the script using it.

```python
from RenesSQLiteHelper import open_db, bulk_load
con = open_db(__file__, 'some-data.db', deleteIfExists = True)

con.execute('''
create table tab (
   id  integer primary key,
   val text
)
''')
```

### Use the databae

```python
con = open_db(__file__, 'some-data.db')

with bulk_load(con) as cur:
    cur.execute('insert into tab values (?, ?)', (42, 'hello world'))
```
