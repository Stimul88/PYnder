import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class VK_Users(Base):
    __tablename__ = "vk_users"
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.String(20), nullable=False)
    first_name = sq.Column(sq.String(20), nullable=False)
    last_name = sq.Column(sq.String(20), nullable=False)
    city = sq.Column(sq.String(20), nullable=False)
    sex = sq.Column(sq.Boolean, nullable=False)
    birth_date = sq.Column(sq.Date, nullable=False)
    url = sq.Column(sq.String(100), nullable=False)
    owner_id = sq.Column(sq.Integer, nullable=False)
    photos = relationship("Photos", back_populates="vk_user")
    favourites = relationship("Favourites", back_populates="vk_user")

class Photos(Base):
    __tablename__ = "photos"
    id = sq.Column(sq.Integer, primary_key=True)
    vk_user_id = sq.Column(sq.Integer, sq.ForeignKey("vk_users.id"), nullable=False)
    url = sq.Column(sq.String(100), nullable=False)
    likes = sq.Column(sq.Integer, nullable=False)
    vk_user = relationship("VK_Users", back_populates="photos")
    owner = relationship("Owners", back_populates="owners")


class Favourites(Base):
    __tablename__ = 'favourites'
    id = sq.Column(sq.Integer, primary_key=True)
    vk_user_id = sq.Column(sq.Integer, sq.ForeignKey("vk_users.id"), nullable=False)
    owner_id = sq.Column(sq.Integer, sq.ForeignKey("owners.id"), nullable=False)
    vk_user = relationship("VK_Users", back_populates="favourites")
    owner = relationship("Owners", back_populates="favourites")


class Owners(Base):
    __tablename__ = 'owners'
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.String(20), nullable=False)
    owner_id = sq.Column(sq.Integer, nullable=False)
    favourites = relationship("Favourites", back_populates="owner")
    vk_users = relationship("VK_Users", back_populates="owner")
