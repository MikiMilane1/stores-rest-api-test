import os
from db import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from flask import Flask, jsonify, request
from flask_restful import Api

from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from resources.home import Home

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.secret_key = "milan123"
api = Api(app)
db.init_app(app)

jwt = JWTManager(app)

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    user = authenticate(data['username'], data['password'])
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token",
                "error": "authorization_required"
            }
        ), 401
    )


api.add_resource(Home, "/")
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, "/register")

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    if app.config['DEBUG']:
        with app.app_context():
            def create_tables():
                db.create_all()

    app.run(port=5000)
