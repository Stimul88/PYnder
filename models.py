import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Owner(Base):
    __tablename__ = "owners"
    vk_owner_id = sq.Column(sq.String(50), primary_key=True)
    favourites = relationship("Favourite", back_populates="owner")


class VKUser(Base):
    __tablename__ = "vk_users"
    vk_user_id = sq.Column(sq.String(50), primary_key=True)
    first_name = sq.Column(sq.String(20), nullable=False)
    last_name = sq.Column(sq.String(20), nullable=False)
    city = sq.Column(sq.String(20), nullable=False)
    sex = sq.Column(sq.Boolean, nullable=False)
    birth_date = sq.Column(sq.Date, nullable=False)
    url = sq.Column(sq.String, nullable=False)
    photos = relationship("Photo", back_populates="vk_user")
    favourites = relationship("Favourite", back_populates="vk_user")

#
class Photo(Base):
    __tablename__ = "photos"
    id = sq.Column(sq.Integer, autoincrement=True, primary_key=True)
    vk_user_id = sq.Column(sq.String(50), sq.ForeignKey("vk_users.vk_user_id"))
    url = sq.Column(sq.String, nullable=False)
    likes = sq.Column(sq.Integer, nullable=False)
    vk_user = relationship("VKUser", back_populates="photos")


class Favourite(Base):
    __tablename__ = "favourites"
    id = sq.Column(sq.Integer, autoincrement=True, primary_key=True)
    vk_user_id = sq.Column(sq.String(50), sq.ForeignKey("vk_users.vk_user_id"), nullable=False)
    vk_owner_id = sq.Column(sq.String(50), sq.ForeignKey("owners.vk_owner_id"), nullable=False)
    vk_user = relationship("VKUser", back_populates="favourites")
    owner = relationship("Owner", back_populates="favourites")
