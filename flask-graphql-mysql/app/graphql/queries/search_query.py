import strawberry
import math
from sqlalchemy import select, func, or_
from typing import List, Optional
from app.models.product import Product, db
from app.graphql.types.productType import ProductType
from graphql import GraphQLError

@strawberry.type
class ProductSearchResponse:
    page: int
    totpage: int
    totalrecords: int
    products: List[ProductType]


@strawberry.type
class ProductSearch():

    @strawberry.field
    def product_search(self, keyword: str, page: int = 1) -> ProductSearchResponse:
        per_page = 5        
        search_term = f"%{keyword.lower()}%"

        queryCnt =  db.session.query(func.count()).select_from(Product)    

        total_records = queryCnt.where(or_(Product.descriptions.ilike(search_term))).scalar()
        if total_records == 0:
            raise GraphQLError(f"No record(s) found.")


        total_pages = math.ceil(total_records / per_page)    

        stmt = select(Product).where(Product.descriptions.ilike(search_term))

        pagination = db.paginate(
            stmt, 
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
                alertstocks=item.alertstocks,
                productpicture=item.productpicture,
                criticalstocks=item.criticalstocks
            ) for item in pagination.items
        ]

        return ProductSearchResponse(
            page=page,
            totpage=total_pages,
            totalrecords=total_records,
            products=product_data
        )

# =====REQUEST======
# query ProductSearch($keyword: String!, $page: Int!) {
#   product_search(keyword: $keyword, page: $page) {    
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

# ====VARIABLES====
# {
#   	"keyword": "cineo",
#     "page": 1
# }
