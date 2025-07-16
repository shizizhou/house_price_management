from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from flask_login import UserMixin

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    properties = relationship("Property", back_populates="owner")


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    location = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="properties")