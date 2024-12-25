from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# User model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    username = db.Column(db.String(100), nullable=False, unique=True)  # Unique username
    email = db.Column(db.String(150), nullable=False, unique=True)  # Unique email
    password = db.Column(db.String(200), nullable=False)  # Password (hashed)
    goals = db.relationship('Goal', backref='user', lazy=True)
    progresses = db.relationship('Progress', backref='user', lazy=True)
    skills = db.relationship('Skill', backref='user', lazy=True)

# Goal model


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Progress model
class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the progress entry
    date = db.Column(db.Date, nullable=False)  # Date of progress entry
    description = db.Column(db.String(200))  # Description of progress made
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Skill model (optional)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the skill
    name = db.Column(db.String(100), nullable=False)  # Name of the skill
    description = db.Column(db.String(200))  # Optional description
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Generated by OpenAI ChatGPT