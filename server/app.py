#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

def find_restaurant_by_id (id):
    return Restaurant.query.where(Restaurant.id == id).first()
# GET /restaurants 

@app.get('/restaurants')
def get_all_restaurants():
    
    all_restaurants = Restaurant.query.all()
    restaurant_dicts = [restaurant.to_dict(rules = ['-restaurant_pizzas',]) for restaurant in all_restaurants]
    return restaurant_dicts, 200

@app.get("/restaurants/<int:id>")
def get_restaurant_by_id(id):
    #1 find restaurant with that id
    found_restaurant = find_restaurant_by_id(id)
    
       #too troubleshoot for none ids 
    if found_restaurant:
        
    #2 send it to the user (client)
        return found_restaurant.to_dict(), 200
    
    else:
        #3 send a 404 if it doesnt exist
        return {"error": "Restaurant not found"}, 404
    
@app.get('/pizzas')
def get_all_pizzas():
    
    all_pizzas = Pizza.query.all()
    pizza_dicts = [pizza.to_dict(rules = [ '-restaurant_pizzas',]) for pizza in all_pizzas]
    return pizza_dicts, 200
   
@app.post('/restaurant_pizzas')
def create_new_restaurant_pizza():
    
    body_data = request.json 
    price = body_data.get('price')
    pizza_id = body_data.get('pizza_id')
    restaurant_id = body_data.get('restaurant_id')
    
    if price is None or pizza_id is None or restaurant_id is None:
        return {"errors": ['Price,pizza_id and restaurant_id are required']}, 400
    if not (1 <= price <= 30):
        return {"errors": ['validation errors']}, 400
    try:
        new_restaurant_pizza = RestaurantPizza(
            price = price,
            pizza_id = pizza_id,
            restaurant_id = restaurant_id
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        
        return new_restaurant_pizza.to_dict(),201
    
    except Exception as e:
        return {"errors": [str(e)]},500
        
@app.delete('/restaurants/<int:id>')
def delete_restaurant_by_id(id):
    found_restaurant = find_restaurant_by_id(id)
    if found_restaurant:
        db.session.delete(found_restaurant)
        db.session.commit()
        return {}, 204
    else:
        return {"error": 'Restaurant not found'}, 404
    

if __name__ == "__main__":
    app.run(port=5555, debug=True)
