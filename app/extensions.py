from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()


