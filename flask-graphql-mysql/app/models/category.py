from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Numeric, text
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from app.config import db
from flask import jsonify

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    products = db.relationship("Product", back_populates="category_rel")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __repr__(self):
        return f"<Category '{self.id}','{self.name}'>"

# 