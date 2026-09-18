# vim: foldmethod=marker foldmarker={{{,}}}

import sqlite3
from pathlib import Path
import os.path

def open_db(db_name, db_dir = '~/.local/share/sqlite-dbs', deleteIfExists = False): # {{{

  # Add .db suffix if not provided because the standard bash completion
  # for sqlite requires .db so that the file is recognized as sqlite database
    if not db_name.endswith('.db'):
        db_name = db_name + '.db'

    abs_db_path = Path(db_dir).expanduser() / db_name

    Path(db_dir).expanduser().mkdir(parents=False, exist_ok=True)

    db_exists = os.path.isfile(abs_db_path)
    if not deleteIfExists and not db_exists:
     #
     # The user does not want to delete an existing database.
     # Hence, he assumes that the database exists.
     # But the database does not exist.
     # Hence, we return None
     #
       return None

    if db_exists and deleteIfExists:
       os.remove(abs_db_path)

    con = sqlite3.connect(abs_db_path)

  # Enable name-based access to columns in resultsets
    con.row_factory = sqlite3.Row

    con.execute('pragma foreign_keys = on')

    return con
# }}}

class bulk_load: # {{{ Context manager

   def __init__(self, con):
       self.con = con

   def __enter__(self):
       init_bulk_load(self.con)

       cur = self.con.cursor()

       return cur
       
   def __exit__(self, exc_type, exc_val, exc_tb):
       if exc_type:
          print(f'Exception in bulk load. {exc_type.__name__}: {exc_val}')
          self.con.rollback()
          return False

       self.con.commit()
# }}}       

def init_bulk_load(db): # {{{
 #
 # TODO: Of course, when the context manager is done,
 #       these changes should be revereted.
 # TODO: I believe, the parameter db would be more appropriately
 #       be called con, but check if the 2nd parameter in
 #       the constructor.
 #
   db.execute('pragma synchronous=off'    )
   db.execute('pragma cache_size=4000000' )
   db.execute('pragma journal_mode=memory')
# }}}
