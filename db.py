import db_function as dbf
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

engine = sq.create_engine(dbf.get_db_config('db.ini'))
dbf.create_structure(engine)
Session = sessionmaker(bind=engine)
session = Session()
input()
dbf.delete_structure(engine)
