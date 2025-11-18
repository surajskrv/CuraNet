from flask import Flask
from backend.extensions import db
from backend.models import User, Role
from backend.config import LocalDevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore

app = None

def start():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)
    app.app_context().push()
    
    return app
    
app = start()

from backend.createData import *
from backend.routes.authRoutes import *   
from backend.routes.adminRoutes import *   
from backend.routes.patientRoutes import *   
from backend.routes.doctorRoutes import *   

if __name__ == '__main__':
    app.run()