import db_function as dbf
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

engine = sq.create_engine(dbf.get_db_config("db.ini"))
dbf.delete_structure(engine)
dbf.create_structure(engine)
Session = sessionmaker(bind=engine)
session = Session()

vk_user_dict = {
    # "id": 1,
    "vk_user_id": "781362360",
    "first_name": "Test",
    "last_name": "User",
    "city": "Москва",
    "sex": True,
    "birth_date": "30.06.1979",
    "url": "https://vk.com/781362360",
}
images_dict = {
    # "id": 1,
    "vk_user_id": "1",
    "images": [["image1.jpg", 12], ["image2.jpg", 11], ["image3.jpg", 55]],
}

owners_dict = {
    # "id": 1,
    "vk_owner_id": "781362360",}
favourites_dict = {
    # "id": 1,
    "vk_user_id": "1", "vk_owner_id": "1",}

dbf.upload_owner_record(session, owners_dict)
dbf.upload_vk_record(session, vk_user_dict, images_dict)
dbf.upload_favourite_record(session, favourites_dict)
