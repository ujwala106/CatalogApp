import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(Users)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class TouristPlaces(Base):
    __tablename__ = 'places'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship(Country, single_parent=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(Users)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///country_catalog.db')


Base.metadata.create_all(engine)
