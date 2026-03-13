from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Numeric, text
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from app.config import db
from flask import jsonify

class Sale(db.Model, SerializerMixin):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    saleamount = db.Column(db.Numeric(10,2),nullable=False)
    saledate = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'saleamount': self.saleamount,
            'saledate': self.saledate,
        }

    def __repr__(self):
        return f"<Sale '{self.id}','{self.saleamount}','{self.saledate}'>"
