from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/category.json')
def getCategoriesJson():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/category/<int:category_id>/item.json')
def getItemsForCategoryJson(category_id):
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/')
@app.route('/category/<int:category_id>')
def getCatalogPage(category_id=0):
    categories = session.query(Category).all()
    if category_id == 0:
        itemHeading = "Lastest Items"
        items = session.query(Item).order_by(desc(Item.created_at)).limit(10)
    else:
        items = session.query(Item).filter_by(category_id=category_id).all()
        itemHeading = session.query(Category).filter_by(id=category_id) \
            .one().name + " Items (" + str(len(items)) + ")"

    return render_template('catalog.html', categories=categories,
                           selected_category=category_id,
                           itemHeading=itemHeading, items=items)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
