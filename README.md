# RenesSQLiteHelper

René's minimal wrapper around Python's built-in `sqlite3` module.

## Installation

```bash
pip install RenesSQLiteHelper
```

## Usage

### Create a database

The database file (Here: `some-data.db`, the `.db` suffix is
[automatically added if missing](https://github.com/ReneNyffenegger/py-RenesSQLiteHelper/blob/3409e412095e710680bf5415a49d16d1b971799b/RenesSQLiteHelper/__init__.py#L9-L12)) is stored by default under `~/.local/share/sqlite-dbs`.

```python
from RenesSQLiteHelper import open_db, bulk_load
con = open_db('some-data', deleteIfExists = True)

con.execute('''
create table tab (
   id  integer primary key,
   val text
)
''')
```

### Use the database

Bulk load
```python
con = open_db('some-data')

with bulk_load(con) as cur:
    cur.execute('insert into tab values (?, ?)', (42, 'hello world'))
```

Selecting etc
```python
for rec in con.execute('select * from tab'):
    print(f'{rec['id']}: {rec['val']}')
```
