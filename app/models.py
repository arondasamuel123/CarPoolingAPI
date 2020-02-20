from werkzeug.security import generate_password_hash, check_password_hash

from . import db

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    email =db.Column(db.String(255), unique=True)
    public_id = db.Column(db.String(255),unique=True)
    username = db.Column(db.String(255), unique=True)
    pass_secure = db.Column(db.String(255))
    workspaces = db.relationship('Workspace', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    workspaceusers = db.relationship('WorkspaceUser', backref='user', lazy='dynamic')
    
    @property
    def password():
        return AttributeError("Password attribute cannot be read")

    @password.setter
    def password(self, pass_entry):
        self.pass_secure = generate_password_hash(pass_entry)

    def check_password(self, pass_entry):
        return check_password_hash(self.pass_secure, pass_entry)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Workspace(db.Model):
    __tablename__='workspaces'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))
    admin_id = db.Column(db.String(255), db.ForeignKey('users.public_id'))
    description = db.Column(db.String(255))
    cars = db.relationship('Car', backref='workspace', lazy='dynamic')
    workspaceusers = db.relationship('WorkspaceUser', backref='workspace', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete_space(self):
        db.session.delete(self)
        db.session.commit()
    
    
class Car(db.Model):
    __tablename__='cars'
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(255))
    noofseats = db.Column(db.Integer)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id'))
    trips = db.relationship('Trip', backref='car', lazy='dynamic')
class Trip(db.Model):
    __tablename__='trips'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    from_dest= db.Column(db.String(255))
    to_dest = db.Column(db.String(255))
    completed = db.Column(db.Boolean)
    reviews = db.relationship('Review', backref='trip',lazy='dynamic')
class Review(db.Model):
    __tablename__='reviews'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    user_id = db.Column(db.String(255), db.ForeignKey('users.public_id'))
    review = db.Column(db.String(255))
    
class WorkspaceUser(db.Model):
    __tablename__='workspace_user'
    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id'))
    user_id = db.Column(db.String(255), db.ForeignKey('users.public_id'))
    
class ApiResponse():
    def __init__(self, status, data):
        self.status = status
        self.data = data

    def __repr__(self):
        return f"<ApiResponse {status}>"