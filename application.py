from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response, flash
import requests


app = Flask(__name__)


# Use Google Account Info for secure connection
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# Connect to Database and create database session
engine = create_engine('sqlite:///catalog1.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create Anti-forgery state token
# Create a state token to prevent request forgery.
# Store it in the session for later validation.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# This is the Google Connect Procedure
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
        return response

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

    # check user logged in?
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    # modified next line from credentials.access_token to just access_token
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

    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # See if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: \
                  300px;border-radius: 150px;-webkit-border-radius: \
                  150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


# GMAIL DISCONNECT - Revoke a current user's token and reset their
# login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user. Modified next line for access_token
    access_token = login_session['access_token']
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = (make_response(json.dumps
                    ('Failed to revoke token for given user.', 400)))
        response.headers['Content-Type'] = 'application/json'
        return response


# This is the facebook Connect Procedure
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

# Exchange client token for long-lived server side token with GET /oauth/
# access_token?grant_type=fb_exchange_token&client_id={app-
# id}&client_secret={app_secret}&fb_exchange_token={short-lived-token}
#
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    """ Due to the formatting for the result from the server token exchange we
    have to split the token first on commas and select the first index
    which gives us the key : value for the server access token then we
    split it on colons to pull out the actual token value and replace the
    remaining quotes with nothing so that it can be used directly in the
    graph api calls
    """
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.10/me/picture?access_token=%s&redirect=0&height=200&width=200' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '  # noqa

    flash("Now logged in as %s" % login_session['username'])
    return output


# Facebood DISCONNECT - Revoke a current user's token and reset
# their login_session.
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?access_token=%s'
           % (facebook_id, access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'],
                   )
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


# JSON APIs to view a Catalog Information
@app.route('/catalog/<string:category_name>/category/JSON')
def categoryItemsJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_name=category_name).all()
    return jsonify(Items=[i.serialize for i in items])


# JSON API to view a Category's Item
@app.route('/catalog/<string:category_name>/item/<string:item_name>/JSON')
def ItemJSON(category_name, item_name):
    Category_Item = session.query(Item).filter_by(name=item_name).one()
    return jsonify(Category_Item=Category_Item.serialize)


# JSON API to view all Categories
@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# This begins the section containing all the web applicaton handlers
#
# Show all categories
#
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    """This showCatalog handler will diplay the home page for both a user not
    logged in and one for a logged in user.
    """

    categories = session.query(Category).order_by(asc(Category.name))
    # Limit the query to a maximum of 10 and order by the most recent
    # items added, which is identified by the highest id numbers.
    #
    items = session.query(Item).order_by(Item.id.desc()).limit(10)
    if 'username' not in login_session:
        picture = False
        user_name = False
        print 'picture = '
        print picture
        return render_template('publiccatalog.html',
                               categories=categories,
                               items=items,
                               picture=picture,
                               user_name=user_name,
                               )
    else:
        print 'user id name = ' + login_session['username']
        print 'user id email = ' + login_session['email']
        print 'user id picture = ' + login_session['picture']
        picture = login_session['picture']
        return render_template('catalog.html',
                               categories=categories,
                               items=items,
                               picture=picture,
                               user_name=login_session['username'],
                               )


# Create a new Catalog Category.
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    """This newCategory handler will add a new Category to the Database.  Wehn
    selected it will redirect a user not logged in to login in first.

     The GET request will render the template for the new Category.

    The POST request will take the input provided for a new category and if it
    already exists will redirect to the Catalog home page with a flash message.
    If the input provided does not already exists then the new category item is
    added to the database and returns back to the home page with a flash
    message that the category was successfully added.
    """

    # if user is not logged in then redirect them to login.
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        # Assign the name entered on the form to new_category_name
        new_category_name = request.form['name']

        # Use try except to first try and add a new category to the database.
        # If that category exists then show a flash message, otherwide add
        # the new category to the database with a successful flash message.
        #
        try:

            category = (session.query(Category).
                        filter_by(name=new_category_name).
                        one())
            if category.name == new_category_name:
                flash('The Category %s Already Exists, Please choose a new one'
                      % new_category_name)
                print 'made 1'
                return redirect(url_for('showCatalog'))
        except:
            # Add the new category
            print ' login session user id = '
            print login_session['user_id']
            newCategory = (Category(name=request.form['name'],
                           user_id=login_session['user_id']),
                           )
            session.add(newCategory)
            flash('New Category %s Successfully Created' % newCategory.name)
            session.commit()
            print ' 2nd login session user id = '
            print login_session['user_id']
            print '2nd user_id ='
            print newCategory.user_id
            print 'made 2'
            return redirect(url_for('showCatalog'))
    else:
        # Handle the GET request.
        return render_template('newCategory.html',
                               picture=login_session['picture'],
                               user_name=login_session['username'],
                               )


# Edit a category
@app.route('/category/edit/', methods=['GET', 'POST'])
def editCategory():
    """This editCategory handler will allow a user to edit an existing Category.
    When selected it will redirect a user not logged in to login in first.

    The GET request will render the template for the new Category.

    The POST request will take the input provided for a new category and if it
    already exists will redirect to the Catalog home page with a flash message.
    If the input provided does not already exists then the new category item is
    added to the database and returns back to the home page with a flash
    message that the category was successfully added.
    """

    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).order_by(asc(Category.name))
    if request.method == 'POST':
        # If the Save button on the form was selected, retrieve the
        # category_to_edit object.
        if request.form['submit'] == "save":
            if request.form['select']:
                category_name = request.form['select']
                category_to_edit = (session.query(Category).
                                    filter_by(name=category_name).
                                    one())
                # Add the check for user id where the user's id must be the
                # creator in order to edit it this category.  If not then
                # dispay an alert message with that reason, go back to home
                # page.
                #
                if login_session['user_id'] != category_to_edit.user_id:
                    return "<script>function myFunction() {alert('You are not \
                    authorized to edit this category. Please create your own \
                    category in order to edit.'); window.location= \
                    '/catalog';}</script><body onload='myFunction()''>"

            if request.form['name']:
                # If a value was typed in the form, first check to see if it
                # exists and if it does, provide a flash message and go back
                # to the edit sreen to try again.
                #
                edited_category = request.form['name']
                if category_to_edit.name == edited_category:
                    flash('Category %s already exist, please edit again or \
                            hit Cancel below' % category_name)
                    return redirect(url_for('editCategory'))
                else:
                    # If the value from the form does not already exist in the
                    # database add it and provide a flash message back to the
                    # home page.
                    #
                    category_to_edit.name = edited_category
                    category_to_edit.user_id = login_session['user_id']
                    session.add(category_to_edit)
                    session.commit
                    flash(('Category was Successfully edited from %s to %s'
                           % (category_name, edited_category)))
                    print 'made it to flash message'
                    return redirect(url_for('showCatalog'))
            else:
                # If the create of the category leave the field blank and hits
                # the Save button then show the correspoding alert message and
                # go back to the edit page.
                return "<script>function myFunction() {alert('Category field was left blank.  Please enter a new value or hit Cancel below'); window.location='/category/edit/';}</script><body onload='myFunction()''>"  # noqa
        else:
            # If Cancel was selected from the edit form, go back to home page.
            return redirect(url_for('showCatalog'))
    else:
        # Handle the GET request.
        return render_template('editCategory.html',
                               categories=categories,
                               picture=login_session['picture'],
                               user_name=login_session['username'],
                               )


# Delete a category
@app.route('/category/delete/', methods=['GET', 'POST'])
def deleteCategory():
    """This deleteCategory handler is used to delete a Category, when selected
    it will redirect a user not logged in to login in first.

    The GET request will render the template to Delete a Category.

    The POST request will take the input provided using a select option from
    a list of all categories.  If the logged in user is not the orignal creator
    then an alert message will be presented.  If the logged in user is the
    orignal creator then the delete will be performed and the user will be
    redirected to the Catalog home page with a successful flash message.  If
    the Cancel button is selected the user is returned back to the home page.
    """

    print 'deleteCategory'
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).order_by(asc(Category.name))
    if request.method == 'POST':
        # Process when the Save button is selected
        if request.form['submit'] == "save":
            category_name = request.form['select']
            category_to_delete = (session.query(Category).
                                  filter_by(name=category_name).
                                  one())
            # Check user id, you must be original creator in order to edit it.
            # If the user is not the orginal creator send an alert otherwise
            # make the change in the database and go back to the home page.
            if login_session['user_id'] != category_to_delete.user_id:
                return "<script>function myFunction() {alert('You are not authorized to delete this category. Please create your own category in order to be able to delete it.'); window.location='/catalog';}</script><body onload='myFunction()''>"  # noqa
            category_to_delete.name = category_name
            session.delete(category_to_delete)
            session.commit
            flash('Category %s was Successfully deleted' % category_name)
            return redirect(url_for('showCatalog'))
        else:
            # Cancel was selected rom the delete form, go back to home page.
            return redirect(url_for('showCatalog'))
    else:
        # Handle the GET request.
        return render_template('deleteCategory.html',
                               categories=categories,
                               picture=login_session['picture'],
                               user_name=login_session['username'],
                               )


# Show a selected categories list of items (i.e category_name)
@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showCategoryItems(category_name):
    """When this showCategoryItems handler is selected it will redirect a user
    not logged to the public home page using the publiccatitems.html template
    and a logged in user to the home page using the cataglog.html template,
    where it will then show all the items from the specific category that the
    user selected.
    """

    category_usr = (session.query(Category).
                    filter_by(name=category_name).
                    one())
    creator = getUserInfo(category_usr.user_id)
    categories = (session.query(Category).
                  order_by(asc(Category.name)))
    # sort items by ascending order
    items = (session.query(Item).
             filter_by(category_name=category_name).
             order_by(asc(Item.name)))
    if 'username' not in login_session:
        # Display the Public Template or public home page for the category
        # the user selected.
        return render_template('publiccatitems.html',
                               category_name=category_name,
                               items=items,
                               categories=categories,
                               )
    else:
        # Display the home page for a logged in user for the category the user
        # selected.
        return render_template('catalog.html',
                               items=items,
                               categories=categories,
                               picture=login_session['picture'],
                               user_name=login_session['username'],
                               )


# Create a new item for a selected category (i.e category_name)
@app.route('/catalog/item/new/', methods=['GET', 'POST'])
def newItem():
    """This newItem handler will add a New Item to the Database.  When it is
    first selected it will redirect a user not logged in to login in first.

    The GET request will render the template to Edit an Item.

    The POST request will take the input provided from the Category, Item Name
    and the Item Description fields and add it to the database.
    """

    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       category_name=request.form['category_name'],
                       user_id=login_session['user_id'],
                       )
        session.add(newItem)
        session.commit()
        flash('New Item %s Successfully Created' % (newItem.name))
        return redirect(url_for('showCategoryItems',
                                category_name=newItem.category_name))
    else:
        # Handle the GET request.
        return render_template('newitem.html',
                               categories=categories,
                               picture=login_session['picture'],
                               user_name=login_session['username'],
                               )


# Edit a Category item
@app.route('/catalog/<string:category_name>/item/<string:item_name>/edit',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    """This editItem handler is used to edit an Item.  When selected, it
    will redirect a user not logged in to login in first.

    The GET request will render the template to Edit an Item.

    The POST request will take the input provided from the Item Name and Item
    Description fields and overwrite the existing data.  If the logged in user
    is not the orignal creator of the item then an alert message will be
    presented.  If the logged in user is the orignal creator then the edit
    will be performed and the user will be redirected to the
    showItemDescription handler along with a successful flash message.
    """

    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(name=item_name).one()
    category = session.query(Category).filter_by(name=category_name).one()
    # Check to see if the logged in user is the original creator of the item.
    if login_session['user_id'] != editedItem.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit items to this category. Please create your own item in order to edit the item.');window.location='/catalog';}</script><body onload='myFunction()''>"  # noqa
    if request.method == 'POST':
        # When the Save button is selected
        if request.form['button'] == "save":
            if request.form['name']:
                editedItem.name = request.form['name']
            if request.form['description']:
                editedItem.description = request.form['description']
            session.add(editedItem)
            session.commit()
            flash('Category Item Successfully Edited')
            return redirect(url_for('showItemDescription',
                                    category_name=editedItem.category_name,
                                    item_name=editedItem.name,
                                    ))
        else:
            # When the Cancel button is sellected.
            flash('Category Item Edit was Canceled')
            return redirect(url_for('showItemDescription',
                                    category_name=editedItem.category_name,
                                    item_name=editedItem.name,
                                    ))
    else:
        # Handle the GET request to edit an item.
        return render_template('edititem.html',
                               category_name=category_name,
                               item_name=item_name,
                               item=editedItem,
                               picture=login_session['picture'],
                               user_name=login_session['username'],
                               )


# Delete a menu item
@app.route('/category/<string:category_name>/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    """This deleteItem handler is used to delete an Item, when selected
    it will redirect a user not logged in to login in first.

    The GET request will render the template to Delete an Item.

    When a logged in user and the logged in user is also the creator of an Item
    and the user selects the Delete link this POST request will display the
    deleteItem.html template and ask the user if they are sure they want to
    delte the itme.  The User has a Delete and Cancel option.  The Delete and
    Cancel options will take the user back to the home page for that category
    and display a flash message.
    """

    if 'username' not in login_session:
        return redirect('/login')
    category = (session.query(Category).
                filter_by(name=category_name).
                one())
    itemToDelete = (session.query(Item).
                    filter_by(category_name=category_name, name=item_name).
                    one())
    if login_session['user_id'] != itemToDelete.user_id:
        return "<script>function myFunction() {alert('You are not authorized to Delete Items to this category. Please create your own item in order to delete items.');window.location='/catalog';}</script><body onload='myFunction()''>"  # noqa
    if request.method == 'POST':
        # Cancel button was selected
        if request.form['submit'] == "Cancel":
            flash('Delete Category Item was Successfully Canceled')
            return redirect(url_for('showCategoryItems',
                                    category_name=category_name))
        # Delete button was selected
        session.delete(itemToDelete)
        session.commit()
        flash('Category Item Successfully Deleted')
        return redirect(url_for('showCategoryItems',
                                category_name=category_name))
    else:
        # Handle the GET request to Delete an item.
        return render_template('deleteItem.html',
                               category_name=category_name,
                               item_name=item_name,
                               picture=login_session['picture'],
                               user_name=login_session['username'],
                               )


# the temp .html's are working need to add formatting.
# Show an items description given a category name and item name
@app.route('/catalog/<string:category_name>/<string:item_name>')
def showItemDescription(category_name, item_name):
    """When this showItemDescription handler is selected it will redirect a
    user not logged to the public home page of the item description using the
    publicitemdescription.html template and a logged in user to the item
    description page using the itemdescription.html template, where it will
    then display the item and item description for the specific item that the
    user selected.

    A flash message will be displayed if the user is not logged in or not the
    creator of that item.
    """

    category = (session.query(Category).
                filter_by(name=category_name).
                one())
    item = (session.query(Item).
            filter_by(category_name=category_name, name=item_name).
            one())
    creator = getUserInfo(item.user_id)
    if ('username' not in login_session):
        flash('You must be logged in and the creator of this item in order \
               to edit it')
        # show the item for user not logged in.
        return render_template('publicitemdescription.html',
                               item=item,
                               category=category,
                               creator=creator,
                               )
    else:
        # show the item for a logged in user.
        return render_template('itemdescription.html',
                               item=item,
                               category=category,
                               category_name=category_name,
                               creator=creator,
                               picture=login_session['picture'],
                               user_name=login_session['username'],
                               )


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    """This handler serves as a global disconnect procedure that will log a
    user out no matter which provider they logged in with.
    """

    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
app.run(host='0.0.0.0', port=8000)
