import strawberry
from typing import List
from app.models.product import Product, db
from app.graphql.types.productType import ProductType
from app.graphql.types.categoryType import CategoryType
from app.models.product import Product
from app.models.category import Category

@strawberry.type
class CategoryQuery:
    @strawberry.field
    def categories(self) -> List[CategoryType]:
        return db.session.query(Category).all()

    @strawberry.field
    def products(self) -> List[ProductType]:
        # Your existing product query
        return db.session.query(Product).all()

# ==========REQUEST===========
# query {
#   categories {
#     category
#     products {
#       id
#       descriptions
#       qty
#       unit
#       costprice
#       sellprice
#       saleprice
#       productpicture
#       alertstocks
#       criticalstocks
#     }
#   }
# }
