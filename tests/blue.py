from flask import Blueprint

blue_route = Blueprint("page",__name__)

@blue_route.route('/api/blue')
def blueapi():  # put application's code here
    return 'blue api!'

@blue_route.route('/api/blue/hello')
def blueindex():  # put application's code here
    return 'blue index!'
