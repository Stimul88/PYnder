import db_function as dbf
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

engine = sq.create_engine(dbf.get_db_config("db.ini"))
dbf.delete_structure(engine)
dbf.create_structure(engine)
Session = sessionmaker(bind=engine)
session = Session()

vk_user_dict = {
    "vk_user_id": "a781362360",
    "first_name": "Test",
    "last_name": "User",
    "city": "Москва",
    "sex": True,
    "birth_date": "30.06.1979",
    "url": "https://vk.com/781362360",
    "images": [["image1.jpg", 12], ["image2.jpg", 11], ["image3.jpg", 55]],
}

owner_id = '123'

dbf.add_owner(session, owner_id)
dbf.add_favorite(session, vk_user_dict, owner_id)
