import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    user_id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.String(20), nullable=False)
    first_name = sq.Column(sq.String(20), nullable=False)
    last_name = sq.Column(sq.String(20), nullable=False)
    city = sq.Column(sq.String(20), nullable=False)
    sex = sq.Column(sq.Boolean, nullable=False)
    birth_date = sq.Column(sq.Date, nullable=False)
    url = sq.Column(sq.String(100), nullable=False)
    favourite = sq.Column(sq.Boolean, nullable=False)
    photos = relationship("Photos", back_populates="user")


class Photos(Base):
    __tablename__ = "photos"
    photo_id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("users.user_id"), nullable=False)
    url = sq.Column(sq.String(100), nullable=False)
    likes = sq.Column(sq.Integer, nullable=False)
    user = relationship("Users", back_populates="photos")