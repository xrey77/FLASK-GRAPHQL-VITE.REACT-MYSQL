import strawberry
from typing import List
from app.models.user import User, db
from app.graphql.types.userType import UserType


@strawberry.type
class UserQuery:
    @strawberry.field
    def users(self) -> List[UserType]:
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