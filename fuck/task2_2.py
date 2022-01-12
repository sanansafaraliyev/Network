# import 
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db_1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# db
travels = db.Table('travels', 
    db.Column('fl_id', db.Integer, db.ForeignKey('flights.id'), primary_key=True),
    db.Column('pg_id', db.Integer, db.ForeignKey('passengers.id'), primary_key=True)
)

class FlightM(db.Model):
    __tablename__ = "flights"
    id = db.Column(db.Integer, primary_key=True)
    airplane_id = db.Column(db.Integer, db.ForeignKey('airplanes.id'), nullable=False)
    pass_list = db.Column(db.Text, nullable=False)
    passengers = db.relationship('PassengerM', secondary=travels, lazy='subquery', backref=db.backref('flights', lazy=True))

    # dateandtime = db.Column(db.DateTime, nullable=False, default=datetime.now())

class PassengerM(db.Model):
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    
    # var = db.Column(<datatype>, )

class AirplaneM(db.Model):
    __tablename__ = "airplanes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    max_pass = db.Column(db.Integer, nullable=False)
    # flights = db.relationship()

# api
class Airplane(Resource):
    def post(self):
        json = request.get_json(force=True)
        title = json['title']
        max_pass = json['max_pass']
        new_airplane = AirplaneM(title=title, max_pass=max_pass)

        db.session.add(new_airplane)
        db.session.commit()
        
        return json
        

    def delete(self, id):
        airplane = AirplaneM.query.get(id)

        if not airplane:
            return {"status": "Failed"}

        db.session.delete(airplane)
        db.session.commit()

        return {"status": "Success"}

class Passenger(Resource):
    def get(self, id):
        passenger = PassengerM.query.get(id)

        if not passenger:
            return {"message": f"Passenger {id} does not exist"}        

        flights = passenger.flights
        ans = {}
        for flight in flights:
            ans[flight.id] = flight.airplane_id


        return jsonify(ans)

    def post(self):
        json = request.get_json(force=True)
        name = json['name']

        new_pass = PassengerM(name=name)
        db.session.add(new_pass)
        db.session.commit()

        return json


    def delete(self, id):
        passenger = PassengerM.query.get(id)

        if not passenger:
            return {"status": "Failed"}

        db.session.delete(passenger)
        db.session.commit()
        return {"status": "Success"}

        
class Flight(Resource):
    def get(self, id):
        flight = FlightM.query.get(id)

        if not flight:
            return {"message": "Flight does not exist"}

        passengers = flight.passengers
        ans = {}
        for passenger in passengers:
            ans[passenger.id] = {"name": passenger.name}

        return jsonify(ans)

    
    def post(self):
        json = request.get_json(force=True)
        airplane_id = json['airplane_id']
        pass_list = json['pass_list']

        new_flight = FlightM(airplane_id=airplane_id, pass_list=pass_list)
        
        pass_list = pass_list.split(",")
        for passenger in pass_list:
            p = PassengerM.query.get(passenger)
            if p:
                new_flight.passengers.append(p)
        
        db.session.add(new_flight)
        db.session.commit()

        return json


    def delete(self, id):
        flight = FlightM.query.get(id)

        if not flight:
            return {"status": "Failed"}

        db.session.delete(flight)
        db.session.commit()
        return {"status": "Success"}

# add_resource
def main():
    api.add_resource(Airplane, '/api/airplanes', '/api/airplanes/<int:id>')
    api.add_resource(Passenger, '/api/passengers', '/api/passengers/<int:id>')
    api.add_resource(Flight, '/api/flights', '/api/flights/<int:id>')

# main()



if __name__ == "__main__":
    db.create_all()
    main()
    app.run(debug=True)



# curl 'http://localhost:5000/api/airplanes' -d '{"title": "A", "max_pass": 2000}' -X POST -v


# curl 'http://localhost:5000/api/flights' -d '{"airplane_id": 1, "pass_list": "1"}' -X POST -v

# curl 'http://localhost:5000/api/flights/1' -X DELETE -v


# curl 'http://localhost:5000/api/passengers/1' -X GET -v

# curl 'http://localhost:5000/api/flights/1' -X GET -v
