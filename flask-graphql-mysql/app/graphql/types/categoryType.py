import strawberry
from typing import List
from typing import Optional
from app.graphql.types.productType import ProductType
from app.models.product import Product, db

@strawberry.type
class CategoryType:
    id: int
    category: Optional[str] = strawberry.field(resolver=lambda self: self.name) 

    @strawberry.field
    def products(self) -> List[ProductType]:
        return db.session.query(Product).filter(Product.category_id == self.id).all()


