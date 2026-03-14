import strawberry
from typing import List
from sqlalchemy import select, func
from app.models.product import Product, db
from app.graphql.types.productType import ProductType
from graphql import GraphQLError

@strawberry.type
class ProductQuery:
    @strawberry.field
    def products(self) -> List[ProductType]:
        
        total_records = db.session.query(db.func.count(Product.id)).scalar()
        if total_records == 0:
            raise GraphQLError(f"No record(s) found.")

        return db.session.query(Product).all()

# =========REQUEST=============
# query GetProducts {
#   products{
#     id
#     category
#     descriptions
#     qty
#     unit
#     costprice
#     sellprice
#     saleprice
#     productpicture
#     alertstocks
#     criticalstocks
#   }
# }