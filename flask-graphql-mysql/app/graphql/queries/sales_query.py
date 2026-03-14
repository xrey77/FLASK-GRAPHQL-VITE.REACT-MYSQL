import strawberry
from typing import List
from sqlalchemy import select, func
from app.models.sale import Sale, db
from app.graphql.types.saleType import SaleType
from graphql import GraphQLError

@strawberry.type
class SaleQuery:
    @strawberry.field
    def sales(self) -> List[SaleType]:

        total_records = db.session.query(db.func.count(Sale.id)).scalar()
        if total_records == 0:
            raise GraphQLError(f"No record(s) found.")

        return db.session.query(Sale).all()

# =========REQUEST=============
# query GetSales {
#   sales{
#     id
#     saleamount   
#     saledate
#   }
# }