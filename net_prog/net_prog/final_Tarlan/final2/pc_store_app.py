from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///final.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class PCModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cpu = db.Column(db.String(100), nullable=False)
	ram = db.Column(db.String(100), nullable=False)
	ssd = db.Column(db.String(100), nullable=False)
	price = db.Column(db.Float, nullable=False)
	customer_id = db.Column(db.Integer, db.ForeignKey("CustomerModel.id"), nullable=False)
	customer = db.relationship("Customer", backref=db.backref("customers", lazy=True))

	def __repr__(self):
		return f"<PC (CPU = {cpu}, RAM = {ram}, SSD = {ssd}, Price = {price})>"


class CustomerModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), nullable=False)
	surname = db.Column(db.String(128), nullable=False)
	email = db.Column(db.String(128), unique=True, nullable=False)
	pc_id = db.Column(db.Integer, db.ForeignKey("PCModel.id"), nullable=False)
	pc = db.relationship("Customer", backref=db.backref("pcs", lazy=True))

	def __repr__(self):
		return f"<Customer (name = {name}, surname = {surname}, email = {email})>"


class DealModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	deal = db.Column(db.String(256), nullable=False)
	customer_id = db.Column(db.Integer, db.ForeignKey("CustomerModel.id"), nullable=False)
	customer = db.relationship("Customer", backref=db.backref("customers", lazy=True))
	pc_id = db.Column(db.Integer, db.ForeignKey("PCModel.id"), nullable=False)
	pc = db.relationship("Customer", backref=db.backref("pcs", lazy=True))

	def __repr__(self):
		return f"<Deal = {deal}>"


db.create_all()


customer_post_args = reqparse.RequestParser()
customer_post_args.add_argument("name", type=str, help="Name of the customer", required=True)
customer_post_args.add_argument("surname", type=str, help="Surname of the customer", required=True)
customer_post_args.add_argument("email", type=str, help="Email of the customer", required=True)

pc_post_args = reqparse.RequestParser()
pc_post_args.add_argument("cpu", type=str, help="CPU", required=True)
pc_post_args.add_argument("ram", type=str, help="RAM", required=True)
pc_post_args.add_argument("ssd", type=str, help="SSD", required=True)
pc_post_args.add_argument("price", type=float, help="Price", required=True)


deal_post_args = reqparse.RequestParser()
deal_post_args.add_argument("deal", type=str, help="Info about deal", required=True)
deal_post_args.add_argument("customer_id", type=int, help="Customer who bought", required=True)
deal_post_args.add_argument("pc_id", type=int, help="PC bought", required=True)


resource_fields_pc = {
	"id": fields.Integer,
	"cpu": fields.String,
	"ram": fields.String,
	"ssd": fields.String,
	"price": fields.Float
}

resource_fields_customer = {
	"id": fields.Integer,
	"name": fields.String,
	"surname": fields.String,
	"email": fields.String
}


resource_fields_deal = {
	"id": fields.Integer,
	"deal": fields.String,
	"customer_id": fields.Integer,
	"pc_id": fields.Integer
}

class Customers(Resource):
	@marshal_with(resource_fields_customer)
	def get(self, customer_id):
		result = CustomerModel.query.filter_by(id=customer_id).first()
		if not result:
			abort(404, message=f"Could not find customer with ID {customer_id}")
		return result

	@marshal_with(resource_fields_customer)
	def post(self, customer_id):
		args = customer_post_args.parse_args()
		result = CustomerModel.query.filter_by(id=customer_id).first()
		if result:
			abort(409, message=f"Customer ID {customer_id} taken...")

		customer = CustomerModel(id=customer_id, name=args["name"], surname=args["surname"], email=args["email"])
		db.session.add(customer)
		db.session.commit()
		return customer, 201


class PCs(Resource):
	@marshal_with(resource_fields_pc)
	def get(self, pc_id):
		result = PCModel.query.filter_by(id=pc_id).first()
		if not result:
			abort(404, message=f"Could not find PC with ID {pc_id}")
		return result

	@marshal_with(resource_fields_pc)
	def post(self, pc_id):
		args = pc_post_args.parse_args()
		result = CustomerModel.query.filter_by(id=pc_id).first()
		if result:
			abort(409, message=f"PC ID {pc_id} taken...")

		pc = CustomerModel(id=pc_id, cpu=args["cpu"], ram=args["ram"], ssd=args["ssd"], price=args["price"])
		db.session.add(pc)
		db.session.commit()
		return pc, 201

class Deals(Resource):
	@marshal_with(resource_fields_deal)
	def post(self, pc_id):
		args = deal_post_args.parse_args()
		result = DealModel.query.filter_by(id=deal_id).first()
		if result:
			abort(409, message=f"Deal ID {deal_id} taken...")

		deal = DealModel(id=deal_id, customer_id=args["customer_id"], pc_id=args["pc_id"])
		db.session.add(deal)
		db.session.commit()
		return deal, 201

class CustomerRemoved(Resource):
	def delete(self, customer_id):
		customer = CustomerModel.query.filter_by(id=customer_id).first()
		if not customer:
			abort(404, message=f"Could not find customer with ID {customer_id}")
		db.session.delete(customer)
		db.session.commit()
		return "", 204

class PCRemoved(Resource):
	def delete(self, pc_id):
		pc = PCModel.query.filter_by(id=pc_id).first()
		if not pc:
			abort(404, message=f"Could not find PC with ID {pc_id}")
		db.session.delete(pc)
		db.session.commit()
		return "", 204


api.add_resource(Customers, "/customers")
api.add_resource(PCs, "/pcs")
api.add_resource(Deals, "/deals")
api.add_resource(CustomerRemoved, "/customers/<int:customer_id>")
api.add_resource(PCRemoved, "/pcs/<int:pc_id>")
api.add_resource(DealsByCustomer, "/customers/<int:customer_id>/<string:deals>")
api.add_resource(CustomersByPC, "/pcs/<int:pc_id>/<string:customers>")

if __name__ == "__main__":
	app.run(debug=True)