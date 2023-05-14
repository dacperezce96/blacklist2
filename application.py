import os
from flask import Flask
from modelos.modelos import db
from vistas.vistas import VistaBlackList, VistaBlackUser
from flask_restful import Api

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///test.db")
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_context = application.app_context()
app_context.push()

db.init_app(application)
db.create_all()

api = Api(application)
api.add_resource(VistaBlackList, '/blacklists')
api.add_resource(VistaBlackUser, '/blacklists/<string:email>')

@application.route("/ping")
def index():
    return "pong-pong",500

if __name__ == "__main__":
    application.run(host = "0.0.0.0", port = 5000, debug = True)