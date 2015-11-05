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


# Create Soccer category
category = Category(name="Soccer")

session.add(category)
session.commit()

# Create items for Soccer category
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

# Create Hockey category
category = Category(name="Hockey")

session.add(category)
session.commit()

# Create items for Hockey category
item = Item(title="Hockey Stick", description="Stick for playing hockey",
            category=category)

session.add(item)
session.commit()

# Create Basketball category
category = Category(name="Basketball")

session.add(category)
session.commit()

# Create Baseball category
category = Category(name="Baseball")

session.add(category)
session.commit()

# Create items for Baseball category
item = Item(title="Bat", description="Bat for playing baseball",
            category=category)

session.add(item)
session.commit()

# Create Frisbee category
category = Category(name="Frisbee")

session.add(category)
session.commit()

# Create items for Frisbee category
item = Item(title="Frisbee", category=category)

session.add(item)
session.commit()

# Create Snowboarding category
category = Category(name="Snowboarding")

session.add(category)
session.commit()

# Create items for Snowboarding category
item = Item(title="Snowboard", category=category)

session.add(item)
session.commit()

item = Item(title="Goggles",
            description="Goggles for wearing while snowboarding",
            category=category)

session.add(item)
session.commit()

# Create Rock Climbing category
category = Category(name="Rock Climbing")

session.add(category)
session.commit()

# Create Foosball category
category = Category(name="Foosball")

session.add(category)
session.commit()

# Create Skating category
category = Category(name="Skating")

session.add(category)
session.commit()

print "added categories and items in catalog!"
