from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash, Response, abort
from sqlalchemy import create_engine, desc, exc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from xml.etree.ElementTree import Element, tostring
from functools import wraps


# Initialization code
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Helper function for generating a random string
def random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in xrange(32))


# Authentication check function decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            print(request.url)
            return redirect('/login?returnUrl=' + request.path)
        return f(*args, **kwargs)
    return decorated_function


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    return_url = request.args.get('returnUrl')
    if not return_url:
        return_url = '/'
    state = random_string()
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state, return_url=return_url)


# Create anti-forgery state token
@app.route('/logout')
def logout():
    gdisconnect()
    return redirect('/')


# Google OAuth connect function
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += (' " style = "width: 300px; height: 300px;border-radius: 150px;'
               '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> ')
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Google OAuth disconnect function
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # Reset the user's sesson.
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Web method to get catalog data as JSON
@app.route('/catalog.json')
def getCatalogJson():
    catalog_dict = {}
    catalog_dict['categories'] = []
    categories = session.query(Category).all()

    for c in categories:
        category = c.to_dict
        items = session.query(Item).filter_by(category_id=c.id).all()
        category['items'] = [i.to_dict for i in items]
        catalog_dict['categories'].append(category)

    return jsonify(catalog_dict)


# Web method to get catalog data as XML
@app.route('/catalog.xml')
def getCatalogXml():
    root_node = Element("Categories")
    categories = session.query(Category).all()

    for c in categories:
        category_node = c.to_xml
        items_node = Element("Items")
        category_node.append(items_node)
        items = session.query(Item).filter_by(category_id=c.id).all()

        for i in items:
            items_node.append(i.to_xml)

        root_node.append(category_node)

    return Response(tostring(root_node), mimetype='text/xml')


# Web method to display main catalog page
@app.route('/')
@app.route('/catalog')
@app.route('/catalog/<category_name>')
def getCatalogPage(category_name=None):
    category_id = 0
    categories = session.query(Category).order_by(Category.name).all()
    if not category_name:
        itemHeading = "Latest Items"
        items = session.query(Item).order_by(desc(Item.created_at)).limit(10)
    else:
        category_id = session.query(Category).filter_by(name=category_name) \
            .one().id
        items = session.query(Item).filter_by(category_id=category_id) \
            .order_by(Item.title).all()
        itemHeading = category_name + " Items (" + str(len(items)) + ")"

    return render_template('catalog.html', categories=categories,
                           selected_category_id=category_id,
                           itemHeading=itemHeading, items=items,
                           auth_state=authState())


# Web method to handle add item requests
@app.route('/catalog/add', methods=['GET', 'POST'])
@login_required
def addItem():
    categories = session.query(Category).order_by(Category.name).all()
    if request.method == 'POST':
        # CSRF protection
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

        category = session.query(Category) \
            .filter_by(name=request.form['category']).one()
        user = getUserInfo(login_session['user_id'])
        newItem = Item(title=request.form['title'],
                       description=request.form['description'],
                       image_url=request.form['image_url'],
                       category=category, user=user)
        try:
            session.add(newItem)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return render_template('add_or_edit_item.html',
                                   auth_state=authState(),
                                   item=newItem, return_url='/',
                                   categories=categories, title='Add Item',
                                   error_msg="Item '" + newItem.title +
                                   "' already exists in category '" +
                                   category.name + "'")

        return redirect('/')
    else:
        return render_template('add_or_edit_item.html', auth_state=authState(),
                               return_url='/', categories=categories,
                               title='Add Item')


# Web method to display item information page
@app.route('/catalog/<category_name>/<item_title>')
def getItemPage(category_name, item_title):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(title=item_title,
                                         category_id=category.id).one()

    return render_template('item.html', item=item,
                           auth_state=authState())


# Web method to handle edit existing item requests
@app.route('/catalog/<category_name>/<item_title>/edit',
           methods=['GET', 'POST'])
@login_required
def editItem(category_name, item_title):
    categories = session.query(Category).order_by(Category.name).all()
    category, = (c for c in categories if c.name == category_name)
    item = session.query(Item).filter_by(title=item_title,
                                         category_id=category.id).one()

    if item.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not authorized "
                "to edit this item. Please create your own item in order to "
                "edit.');}</script><body onload='myFunction()''>")

    return_url = url_for('getItemPage', category_name=category_name,
                         item_title=item_title)

    if request.method == 'POST':
        # CSRF protection
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

        new_category = session.query(Category) \
            .filter_by(name=request.form['category']).one()
        try:
            item.title = request.form['title']
            item.image_url = request.form['image_url']
            item.description = request.form['description']
            item.category = new_category
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return render_template('add_or_edit_item.html',
                                   auth_state=authState(),
                                   item=item, return_url=return_url,
                                   categories=categories, title='Edit Item',
                                   error_msg="Item '" + item.title +
                                   "' already exists in category '" +
                                   new_category.name + "'")

        # rebuild the return_url in case the item's category and/or title
        # have been modified
        return_url = url_for('getItemPage', category_name=item.category.name,
                             item_title=item.title)

        return redirect(return_url)
    else:
        return render_template('add_or_edit_item.html', auth_state=authState(),
                               item=item, return_url=return_url,
                               categories=categories, title='Edit Item')


# Web method to handle delete existing item requests
@app.route('/catalog/<category_name>/<item_title>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteItem(category_name, item_title):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(title=item_title,
                                         category_id=category.id).one()

    if item.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not authorized "
                "to delete this item. Please create your own item in order to "
                "delete.');}</script><body onload='myFunction()''>")

    return_url = url_for('getItemPage', category_name=category_name,
                         item_title=item_title)

    if request.method == 'POST':
        # CSRF protection
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

        try:
            session.delete(item)
            session.commit()
        except exc.SQLAlchemyError, e:
            session.rollback()
            return render_template('delete.html',
                                   auth_state=authState(),
                                   item=item, return_url=return_url,
                                   error_msg="Item '" + item.title +
                                   "' could not be deleted. Reason: " +
                                   str(e))
        return redirect(url_for('getCatalogPage', category_name=category.name))
    else:
        return render_template('delete_item.html', auth_state=authState(),
                               item=item, return_url=return_url)


# Helper function to get auth state data to be passed to jinja templates
def authState():
    auth_state = {}
    if 'username' in login_session:
        auth_state['username'] = login_session['username']
        auth_state['user_id'] = login_session['user_id']
        auth_state['url'] = '/logout'
        auth_state['text'] = 'Logout'
    else:
        auth_state['url'] = '/login?returnUrl=' + request.path
        auth_state['text'] = 'Login'
    return auth_state


# Generate CSRF protection nonce token
def generate_csrf_token():
    if '_csrf_token' not in login_session:
        login_session['_csrf_token'] = random_string()
    return login_session['_csrf_token']


# Flask app setup
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.jinja_env.globals['csrf_token'] = generate_csrf_token
    app.run(host='0.0.0.0', port=5000)
