from flask import Flask
from .extensions import db
from .models import User, Role
from .config import LocalDevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore

app = None

def start():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)
    app.app_context().push()
    db.create_all()
    
    return app
    
app = start()

from .createData import *
from .routes.authRoutes import *   
from .routes.adminRoutes import *   
from .routes.patientRoutes import *   
from .routes.doctorRoutes import *   

if __name__ == '__main__':
    app.run()
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
