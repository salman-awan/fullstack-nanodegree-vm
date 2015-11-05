from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item


# Create SqlLite engine instance
engine = create_engine('sqlite:///catalog.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# Create SqlAlchemy DB session instance
session = DBSession()


# Create soccer category
category = Category(name="Soccer")

session.add(category)
session.commit()

# Create items for soccer category
item = Item(title="Shinguards", description="Guards for shins",
            category=category,
            image_url=("https://images.rapgenius.com/"
                       "f4f5caebcd3e3822f051ad20ec72966c.300x300x1.jpg"))

session.add(item)
session.commit()

item = Item(title="Soccer Shoes", description="Shoes for playing soccer",
            category=category,
            image_url=("http://www.okokchina.com/Files/uppic45/"
                       "SOCCER%20SHOES132.jpg"))

session.add(item)
session.commit()

# Create hockey category
category = Category(name="Hockey")

session.add(category)
session.commit()

# Create items for hockey category
item = Item(title="Hockey Stick", description="Stick for playing hockey",
            category=category)

session.add(item)
session.commit()

print "added categories and items in catalog!"
