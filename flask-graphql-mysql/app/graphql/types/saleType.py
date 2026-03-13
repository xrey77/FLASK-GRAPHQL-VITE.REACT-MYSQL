import strawberry
from datetime import datetime 
from typing import Optional
from decimal import Decimal

@strawberry.type
class SaleType:
    id: strawberry.ID
    saleamount: Decimal
    saledate: datetime