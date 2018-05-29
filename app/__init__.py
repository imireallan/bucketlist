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

    @app.route("/bucketlists", methods=["GET"])
    def get_all_bucketlists():
        bucketlists = bucketlist.get_all()
        if not bucketlists:
            abort(404)
            return make_response(jsonify({"message": "bucketlist not found"}), 404)
        results = []
        for bucketlist in bucketlists:
            obj = {
                "id": bucketlist.id,
                "name": bucketlist.name,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route("/bucketlists/<int:id>", methods="GET")
    def get_one(id):
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)
            return make_response(jsonify({"message":"bucketlist with id {} not found".format(bucketlist.id)}), 404)

        response = jsonify({
            "id": bucketlist.id,
            "name": bucketlist.name,
            "date_created": bucketlist.date_created,
            "date_modified": bucketlist.date_modified
        })
        response.status_code = 200
        return response

        @app.route("/bucketlists/<int:id>", methods="PUT")
        def update_one(id):
            bucketlist = Bucketlist.query.filter_by(id=id).first()
            if not bucketlist:
                abort(404)
                return make_response(jsonify({"message":"bucketlist with id {} not found".format(bucketlist.id)}), 404)
            
            name = str(request.data.get("name", ""))
            bucketlist.name = name
            bucketlist.save()

            response = jsonify({
                "id": bucketlist.id,
                "name": bucketlist.name,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified
            })
            response.status_code = 200
            return response



    return app