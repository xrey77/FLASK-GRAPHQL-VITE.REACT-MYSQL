import strawberry
from typing import List
from app.models.product import Product, db
from app.graphql.types.productType import ProductType

@strawberry.type
class ProductQuery:
    @strawberry.field
    def products(self) -> List[ProductType]:
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