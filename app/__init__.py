# third-party imports
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, make_response, abort

# local imports
from instance.config import app_config

# instantiating the db
db = SQLAlchemy()

def create_app(config_name):
    """Instantiating the app and its configurations"""
    from models import Bucketlist
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")

    db.init_app(app)

    @app.route("/bucketlists/", methods=["POST"])
    def create_bucketlists():
        name = str(request.data.get("name",""))
        bucketlist = Bucketlist(name=name)
        bucketlist.save()
        response = jsonify({
            "id": bucketlist.id,
            "name": bucketlist.name,
            "date_created": bucketlist.date_created,
            "date_modified": bucketlist.date_modified
        })
        response.status_code = 201
        return response


    return app