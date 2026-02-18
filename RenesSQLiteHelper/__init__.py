# vim: foldmethod=marker foldmarker={{{,}}}

import sqlite3
from pathlib import Path
import os.path

def open_db(__file__of_includer, db_name, deleteIfExists = False): # {{{

    abs_db_path = Path(__file__of_includer).absolute().parent / db_name

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
          print(f'exception in bulk load. {exc_type.__class__}')
          self.con.rollback()
          return False

       self.con.commit()
# }}}       

def init_bulk_load(db): # {{{
   db.execute('pragma synchronous=off'    )
   db.execute('pragma cache_size=4000000' )
   db.execute('pragma journal_mode=memory')
# }}}
