from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
category = Category(name="Soccer")

session.add(category)
session.commit()

item = Item(title="Shinguards", description="Guards for shins",
            category=category)

session.add(item)
session.commit()

item = Item(title="Soccer Shoes", description="Shoes for playing soccer",
            category=category)

session.add(item)
session.commit()

category = Category(name="Hockey")

session.add(category)
session.commit()

item = Item(title="Hockey Stick", description="Stick for playing hockey",
            category=category)

session.add(item)
session.commit()

print "added categories and items in catalog!"
