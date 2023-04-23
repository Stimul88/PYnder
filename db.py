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
}
images_dict = {
    "vk_user_id": "a781362360",
    "images": [["image1.jpg", 12], ["image2.jpg", 11], ["image3.jpg", 55]],
}

owners_dict = {
    "vk_owner_id": "a123123",
}
favorites_dict = {
    "vk_user_id": "a781362360",
    "vk_owner_id": "a123123",
}

print(dbf.upload_owner(session, owners_dict))
print(dbf.upload_vk(session, vk_user_dict))
print(dbf.upload_images(session, images_dict))
print(dbf.upload_favorite(session, favorites_dict))
