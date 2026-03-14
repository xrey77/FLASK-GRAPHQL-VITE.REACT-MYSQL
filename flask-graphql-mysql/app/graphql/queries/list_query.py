import strawberry
import math
from sqlalchemy import select, func
from typing import List, Optional
from app.models.product import Product, db
from app.graphql.types.productType import ProductType
from graphql import GraphQLError

@strawberry.type
class ProductListResponse:
    page: int
    totpage: int
    totalrecords: int
    products: List[ProductType]


@strawberry.type
class ProductList():
    @strawberry.field
    def product_list(self, page: int = 1) -> ProductListResponse:
        per_page = 5        
        total_records = db.session.query(db.func.count(Product.id)).scalar()
        if total_records == 0:
            raise GraphQLError(f"No record(s) found.")

        total_pages = math.ceil(total_records / per_page)    
        pagination = db.paginate(
            db.select(Product).order_by(Product.id), 
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        product_data = [
            ProductType(
                id=item.id, 
                category=item.category, 
                descriptions=item.descriptions,
                qty=item.qty,
                unit=item.unit,
                costprice=item.costprice,
                sellprice=item.sellprice,
                saleprice=item.saleprice,
                productpicture=item.productpicture,
                alertstocks=item.alertstocks,
                criticalstocks=item.criticalstocks
            ) for item in pagination.items
        ]

        return ProductListResponse(
            page=page,
            totpage=total_pages,
            totalrecords=total_records,
            products=product_data
        )

# =========REQUEST==============
# query ProductList($page: Int!) {
#   product_list(page: $page) {    
#     page
#     totpage
#     totalrecords
#     products {
#       id
#       category
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

# =====VARIABLES=====
# {
#     "page": 1
# }
