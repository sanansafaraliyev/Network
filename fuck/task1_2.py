# 12:30

import re
from flask import Flask, request
from flask.json import jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from werkzeug.routing import parse_converter_args

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_db_1.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

class DealModel(db.Model):
    __tablename__ = "deals"
    id = db.Column(db.Integer, primary_key=True)
    pc_id = db.Column(db.Integer, db.ForeignKey("pcs.id"), nullable=False)
    pc = db.relationship("PCModel", backref="deals", lazy=True)
    cs_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    cs = db.relationship("CustomerModel", backref="deals", lazy=True)


class PCModel(db.Model):
    __tablename__ = "pcs"
    id = db.Column(db.Integer, primary_key=True)
    cpu = db.Column(db.String(20), nullable=False)
    ram = db.Column(db.String(20), nullable=False)
    ssd = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    # cs = db.relationship("DealModel", backref="pcs", lazy=True)
    # clients = db.relationship("CustomerModel", secondary=deals, lazy="subquery", backref=db.backref("pcs", lazy="subquery"))

class CustomerModel(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    # pcs = db.relationship("PCModel", backref="deals", lazy=True)


class PC(Resource):
    def get(self, id):
        pc = PCModel.query.get(id)

        if not pc:
            return {"status": "failed", "message": f"pc {id} does not exist"}

        deals = pc.deals
        customers = {}
        for deal in deals:
            customer = deal.cs
            customers[customer.id] = {"name": customer.name, "surname": customer.surname}

        return jsonify(customers)

    def delete(self, id):
        pc = PCModel.query.get(id)

        if not pc:
            return {"status": "failed", "message": f"pc {id} does not exist"}
        
        db.session.delete(pc)
        db.session.commit()

        return {"status": "success", "message": f"pc {id} is deleted successfully"}

    def post(self):
        json = request.get_json(force=True)
        cpu = json["cpu"]
        ram = json["ram"]
        ssd = json["ssd"]
        price = json["price"]

        pc = PCModel(cpu=cpu, ram=ram, ssd=ssd, price=price)

        db.session.add(pc)
        db.session.commit()

        return json


class Customer(Resource):

    def get(self, id):
        customer = CustomerModel.query.get(id)

        if not customer:
            return {"status": "failed", "message": f"customer {id} does not exist"}

        deals = customer.deals
        pcs = {}
        for deal in deals:
            pc = deal.pc
            pcs[pc.id] = {"cpu": pc.cpu, "ram": pc.ram, "ssd": pc.ssd, "price": pc.price}
        
        return jsonify(pcs)

    def delete(self, id):
        customer = CustomerModel.query.get(id)

        if not customer:
            return {"status": "failed", "message": f"customer {id} does not exist"}
        
        db.session.delete(customer)
        db.session.commit()

        return {"status": "success", "message": f"customer {id} is deleted successfully"}


    def post(self):
        json = request.get_json(force=True)
        name = json["name"]
        surname = json["surname"]
        email = json["email"]

        cs = CustomerModel(name=name, surname=surname, email=email)

        db.session.add(cs)
        db.session.commit()

        return jsonify(json)

class Deal(Resource):
    def post(self):
        json = request.get_json(force=True)
        pc_id = json["pc_id"]
        cs_id = json["cs_id"]
        pc = PCModel.query.get(pc_id)
        cs = CustomerModel.query.get(cs_id)

        if not pc or not cs:
            return {"message": f"pc {pc_id} or cs {cs_id} does not exist"}
        
        deal = DealModel(pc_id=pc_id, pc=pc, cs_id=cs_id, cs=cs)

        db.session.add(deal)
        db.session.commit()

        return json

class BestBuyer(Resource):
    def get(self):
        customers = CustomerModel.query.all()

        bestbuyers = []
        max_price = 0

        for customer in customers:
            deals = customer.deals
            price = 0
            for deal in deals:
                pc = deal.pc
                price += pc.price
            
            if price > max_price:
                max_price = price
                bestbuyers = [f"{customer.name} {customer.surname}"]
            elif price == max_price:
                bestbuyers.append(f"{customer.name} {customer.surname}")

        message = f"Bestbuyers are {bestbuyers} with ${max_price} purchase"
        return {"message": message}

def main():
    api.add_resource(PC, "/api/pcs", "/api/pcs/<int:id>")
    api.add_resource(Customer, "/api/customers", "/api/customers/<int:id>")
    api.add_resource(Deal, "/api/deals")
    api.add_resource(BestBuyer, "/api/bestbuyer")
    
if __name__ == "__main__":
    db.create_all()
    main()
    app.run(debug=True)


# curl "http://localhost:5000/api/pcs" -d "{"cpu": "i5", "ssd": "128", "ram": "4", "price": 700}" -X POST -v
# curl "http://localhost:5000/api/pcs" -d "{"cpu": "i7", "ssd": "128", "ram": "8", "price": 1000}" -X POST -v

# curl "http://localhost:5000/api/customers" -d "{"name":"Turgut", "surname": "Agha", "email": "t@t.com"}" -X POST -v
# curl "http://localhost:5000/api/customers" -d "{"name":"Murad", "surname": "Sharif", "email": "m@m.com"}" -X POST -v

# curl "http://localhost:5000/api/deals" -d "{"pc_id": 1, "cs_id": 1}" -X POST -v
# curl "http://localhost:5000/api/deals" -d "{"pc_id": 2, "cs_id": 1}" -X POST -v

# curl "http://localhost:5000/api/customers/1" -X GET -v

# curl "http://localhost:5000/api/pcs/1" -X GET -v

# curl "http://localhost:5000/api/bestbuyer" -X GET -v