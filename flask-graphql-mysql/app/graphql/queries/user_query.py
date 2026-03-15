import strawberry
from typing import List
from sqlalchemy import select, func
from app.models.user import User, db
from app.graphql.types.userType import UserType
from graphql import GraphQLError
from app.services.isAuthenticated import IsAuthenticated

@strawberry.type
class UserQuery:

    @strawberry.field(permission_classes=[IsAuthenticated])    
    def users(self) -> List[UserType]:        
        total_records = db.session.query(db.func.count(User.id)).scalar()
        if total_records == 0:
            raise GraphQLError(f"No record(s) found.")

        return db.session.query(User).all()

# ======REQUEST=======
# query GetUsers {
#   users{
#     id
#     firstname
#     lastname
#     email
#     mobile
#     isactivated
#     isblocked
#     mailtoken
#     userpic
#     qrcodeurl  
#     role_id
#   }
# }