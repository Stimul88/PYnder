import db_function as dbf
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

import test_import

engine = sq.create_engine(dbf.get_db_config("db.ini"))
dbf.delete_structure(engine)
dbf.create_structure(engine)
Session = sessionmaker(bind=engine)
session = Session()

test_import.import_test_data(session)
dbf.delete_favorite(session, '222', '4')
