'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
from server import db
from bottle import request,response

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

# TODO: for test only, only 1 user can login to the system, need a session to replace this.
user = False


#-----------------------------------------------------------------------------
# Register
#-----------------------------------------------------------------------------

def register_form():
    return page_view("Register",suc=True, msg = "",user=user)

#-----------------------------------------------------------------------

# Check the register credentials
def register_check(username, password, c_password, email):
    '''
        register check
        TODO:
        constraints:
            1. No special chars (prevent sqli)
            2. regex uni email
            3. password length
            4. name length
            5. no repeat name
    '''

    if(password!=c_password):
        return page_view("Register",msg = "the 2 entered password are different", suc = False, user=user)

    if get_user_by_name(username):
        return page_view("Register",msg = "name repeated", suc = False, user=user)



    register = db.add_user(username,password,email)
    return login_check(username,password)

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():

    return page_view("index",msg = "",suc = True, user=user)

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------
#
# def login_form():
#     '''
#         login_form
#         Returns the view for the login_form
#     '''
#     return page_view("login")

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    login = db.check_credentials(username,password)

    if login:
        global user
        user=username
        response.set_cookie("myKey",username)
        return page_view("dashboard", msg = "", suc = True, user=user)
    else:
        return page_view("index",msg = "password or username incorrect", suc = False, user=user)

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''

    username_from_cookie = request.get_cookie("myKey",user)
    return page_view("about", garble=about_garble(),msg = "", suc = True, user=username_from_cookie)



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.",
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]

#-----------------------------------------------------------------------------
# Dashboard
#-----------------------------------------------------------------------------
def dashboard():

    return page_view("dashboard.html",msg = "", suc = True, user=user)



#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg,msg = "", suc = True, user=user)


#-----------------------------------------------------------------------------
# get user based on name
#-----------------------------------------------------------------------------

def get_user_by_name(username):

    user = db.get_user_by_name(username)
    return user
