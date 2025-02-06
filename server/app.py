from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, Restaurant, Pizza, RestaurantPizza
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route("/")
def index():
    return "<h1>Code Challenge: Pizza API</h1>"

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200

@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify({
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "restaurant_pizzas": [
            {
                "id": rp.id,
                "price": rp.price,
                "pizza_id": rp.pizza_id,
                "restaurant_id": rp.restaurant_id,
                "pizza": rp.pizza.to_dict()
            }
            for rp in restaurant.restaurant_pizzas
        ]
    }), 200

@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    db.session.delete(restaurant)
    db.session.commit()
    return "", 204  

@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas]), 200

@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()

    if not all(k in data for k in ["price", "pizza_id", "restaurant_id"]):
        return jsonify({"errors": ["Missing required fields"]}), 400

    try:
        new_restaurant_pizza = RestaurantPizza(
            price=data["price"],
            pizza_id=data["pizza_id"],
            restaurant_id=data["restaurant_id"]
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return jsonify(new_restaurant_pizza.to_dict()), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)
