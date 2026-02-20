# RenesSQLiteHelper

René's minimal wrapper around Python's built-in `sqlite3` module.

## Installation

```bash
pip install RenesSQLiteHelper
```

## Usage

### Create a database

The database file (Here: `some-data`) is stored by default under `~/.local/share/sqlite-dbs`.

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
