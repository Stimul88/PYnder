import db_function as dbf
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

my_pynder = dbf.PYnder_DB()

# engine = sq.create_engine(dbf.get_db_config("db.ini"))
# dbf.delete_structure(engine)
# dbf.create_structure(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

my_pynder.import_test_data()

my_pynder.delete_favorite("222", "4")
print(my_pynder.is_in_favorite("a781362360", "3_owner"))
