from .database import db
from flask_security import UserMixin, RoleMixin


roles_users=db.Table('roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('user.id')), db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
  __tablename__= 'user'
  id=db.Column(db.Integer, primary_key=True, autoincrement=True)
  username=db.Column(db.String, unique=True)
  email=db.Column(db.String, unique=True)
  password=db.Column(db.String(255))
  active=db.Column(db.Boolean())
  fs_uniquifier=db.Column(db.String(255), unique=True, nullable=False)
  last_booking_date=db.Column(db.String)
  roles=db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
  __tablename__='role'
  id=db.Column(db.Integer, primary_key=True)
  name=db.Column(db.String, unique=True)
  description=db.Column(db.String)

class theatre(db.Model):
  __tablename__ = 'theatre'
  theatre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  theatre_name= db.Column(db.String, unique=True, nullable=False)
  place= db.Column(db.String, nullable=False)
  location=db.Column(db.String, nullable=False)
  capacity=db.Column(db.Integer)
  shows=db.relationship('show', backref='theatre', lazy=True)

class show(db.Model):
  __tablename__='show'
  show_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
  show_name=db.Column(db.String, nullable=False)
  show_start_timing=db.Column(db.String, nullable=False)
  show_tags=db.Column(db.String)
  price=db.Column(db.Integer, nullable=False)
  theatre_id=db.Column(db.Integer, db.ForeignKey('theatre.theatre_id'))

class bookings(db.Model):
  __tablename__ = 'bookings'
  booking_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
  show_id=db.Column(db.Integer, db.ForeignKey('show.show_id'))
  rating=db.Column(db.Integer)
  tickets_booked=db.Column(db.Integer, nullable=False)
  booked_on=db.Column(db.String)
