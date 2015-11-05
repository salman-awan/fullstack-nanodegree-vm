import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, \
    UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from xml.etree.ElementTree import Element

Base = declarative_base()


# SQLAlchemy declarative class for user table
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

    @property
    def to_xml(self):
        user_node = Element("User")

        child_node = Element("Id")
        child_node.text = str(self.id)
        user_node.append(child_node)

        child_node = Element("Name")
        child_node.text = str(self.name)
        user_node.append(child_node)

        child_node = Element("Email")
        child_node.text = str(self.email)
        user_node.append(child_node)

        return user_node


# SQLAlchemy declarative class for category table
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @property
    def to_xml(self):
        category_node = Element("Category")

        child_node = Element("Id")
        child_node.text = str(self.id)
        category_node.append(child_node)

        child_node = Element("Name")
        child_node.text = str(self.name)
        category_node.append(child_node)

        return category_node


# SQLAlchemy declarative class for item table
class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(250))
    created_at = Column(DateTime(True), default=datetime.datetime.utcnow)
    image_url = Column(String(2000))
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    __table_args__ = (UniqueConstraint('title', 'category_id'),
                      )

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat() + 'Z',
            'image_url': self.image_url,
            'category_id': self.category_id,
            'user': self.user.to_dict if self.user else None,
        }

    @property
    def to_xml(self):
        item_node = Element("Item")

        child_node = Element("Id")
        child_node.text = str(self.id)
        item_node.append(child_node)

        child_node = Element("Title")
        child_node.text = str(self.title)
        item_node.append(child_node)

        child_node = Element("Description")
        child_node.text = xstr(self.description)
        item_node.append(child_node)

        child_node = Element("CreatedAt")
        child_node.text = str(self.created_at.isoformat() + 'Z')
        item_node.append(child_node)

        child_node = Element("ImageUrl")
        child_node.text = xstr(self.image_url)
        item_node.append(child_node)

        child_node = Element("CategoryId")
        child_node.text = str(self.category_id)
        item_node.append(child_node)

        if self.user:
            user_node = self.user.to_xml
            item_node.append(user_node)

        return item_node


# Help function for handling None type string conversion
def xstr(s):
    return '' if s is None else str(s)


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
