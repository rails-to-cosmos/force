"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask.ext.cache import Cache
from flask.ext.mongoengine import MongoEngine
from flask_admin import Admin
from flask.ext.mail import Mail
from flask.ext.debugtoolbar import DebugToolbarExtension

db = MongoEngine()
cache = Cache()
admin = Admin(name='Project Enferno :: Administration')
mail = Mail()
debug_toolbar = DebugToolbarExtension()
