from Flask inport flask
from flask_sqlalchemy import SQLAlchemy



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(120))
    message = db.Column(db.String(200))

    def __init__(self,subject,message):
        self.subject = subject
        self.message = message



    
