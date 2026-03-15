from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Numeric, text
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from app.config import db
from flask import jsonify

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32),nullable=False)
    lastname = db.Column(db.String(32),nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True)
    mobile = db.Column(db.String(32), nullable=True)
    username = db.Column(db.String(32),nullable=False, unique=True)
    password = db.Column(db.String(200),nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, server_default="1")    

    isactivated = db.Column(db.Integer, server_default=text("1"))
    isblocked = db.Column(db.Integer, server_default=text("0"))
    mailtoken = db.Column(db.Integer, server_default=text("0"))
    userpic = db.Column(String(100), server_default="pix.png")    
    secret = db.Column(db.Text, nullable=True)
    qrcodeurl = db.Column(db.Text, nullable=True)    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    role = db.relationship("Role", back_populates="users")        
    
    def to_dict(self, secret=None, qrcodeurl=None):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'mobile': self.mobile,            
            'username': self.username,
            'roles': self.roles,
            'isactivated': self.isactivated,
            'iblocked': self.isblocked,
            'mailtoken': self.mailtoken,
            'userpic': self.userpic,
            'secret': self.secret,
            'qrcodeurl': self.qrcodeurl
        }

    def __repr__(self):
        return f"<User {self.username}>"
    
