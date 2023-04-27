import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Owner(Base):
    __tablename__ = "owners"
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.String(50), nullable=False)
    favorites = relationship("Favorite", back_populates="owner")


class VKUser(Base):
    __tablename__ = "vk_users"
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.String(50), nullable=False)
    first_name = sq.Column(sq.String(20), nullable=False)
    last_name = sq.Column(sq.String(20), nullable=False)
    city = sq.Column(sq.String(20), nullable=False)
    sex = sq.Column(sq.Boolean, nullable=False)
    birth_date = sq.Column(sq.Date, nullable=False)
    url = sq.Column(sq.String, nullable=False)
    photos = relationship("Photo", back_populates="vk_user")
    favorites = relationship("Favorite", back_populates="vk_user")


class Photo(Base):
    __tablename__ = "photos"
    id = sq.Column(sq.Integer, autoincrement=True, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("vk_users.id"))
    url = sq.Column(sq.String, nullable=False)
    likes = sq.Column(sq.Integer, nullable=False)
    vk_user = relationship("VKUser", back_populates="photos")


class Favorite(Base):
    __tablename__ = "favorites"
    id = sq.Column(sq.Integer, autoincrement=True, primary_key=True)
    user_id = sq.Column(
        sq.Integer, sq.ForeignKey("vk_users.id"), nullable=False
    )
    owner_id = sq.Column(
        sq.Integer, sq.ForeignKey("owners.id"), nullable=False
    )
    vk_user = relationship("VKUser", back_populates="favorites")
    owner = relationship("Owner", back_populates="favorites")
