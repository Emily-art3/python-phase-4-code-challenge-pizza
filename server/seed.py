from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():

    print("Deleting existing data...")
    db.session.query(RestaurantPizza).delete()
    db.session.query(Pizza).delete()
    db.session.query(Restaurant).delete()
    db.session.commit()  

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="123 Main St")
    bistro = Restaurant(name="Sanjay's Pizza", address="456 Elm St")
    palace = Restaurant(name="Kiki's Pizza", address="789 Oak St")

    restaurants = [shack, bistro, palace]
    db.session.add_all(restaurants)
    db.session.commit()

    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")

    pizzas = [cheese, pepperoni, california]
    db.session.add_all(pizzas)
    db.session.commit()

    print("Creating RestaurantPizza relationships...")
    rp1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=10)
    rp2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=15)
    rp3 = RestaurantPizza(restaurant=palace, pizza=california, price=20)

    db.session.add_all([rp1, rp2, rp3])
    db.session.commit()

    print("Seeding done successfully!")
