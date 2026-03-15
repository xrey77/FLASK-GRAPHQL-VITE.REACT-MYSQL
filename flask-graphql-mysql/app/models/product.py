from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Numeric, text
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from app.config import db
from flask import jsonify

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50),nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    descriptions = db.Column(db.String(50),nullable=False, unique=True)
    qty= db.Column(db.Integer, server_default=text("0"))
    unit = db.Column(db.String(10),nullable=False)
    costprice = db.Column(db.Numeric(10,2),nullable=False, server_default=text("0.00"))
    sellprice = db.Column(db.Numeric(10,2),nullable=False, server_default=text("0.00"))
    saleprice = db.Column(db.Numeric(10,2),nullable=False, server_default=text("0.00"))    
    alertstocks = db.Column(db.Integer, server_default=text("0"))
    criticalstocks = db.Column(db.Integer, server_default=text("0"))
    productpicture = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())        
    category_rel = db.relationship("Category", back_populates="products")        

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'descriptions': self.descriptions,
            'qty': self.qty,
            'unit': self.unit,
            'costprice': self.costprice,
            'sellprice': self.sellprice,
            'saleprice': self.saleprice,
            'productpicture': self.productpicture,
            'alertstocks': self.alertstocks,
            'criticalstocks': self.criticalstocks,
        }

    def __repr__(self):
        return f"<Product '{self.descriptions}'>"
