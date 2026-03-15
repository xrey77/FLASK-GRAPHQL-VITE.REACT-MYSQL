import strawberry
from typing import Optional
from strawberry.types import Info
from app.models.user import User, db
from app.graphql.types.userType import UserType
from graphql import GraphQLError
from app.services.isAuthenticated import IsAuthenticated

@strawberry.type
class GetUserId():
    @strawberry.field(permission_classes=[IsAuthenticated])    
    def user(self, id: strawberry.ID, info: Info) -> Optional[UserType]:
        user_model = db.session.get(User, id) 
        if not user_model:
            raise GraphQLError(f"User ID not found.")
            
        return UserType(
            id=user_model.id,
            firstname=user_model.firstname,
            lastname=user_model.lastname,
            email=user_model.email,
            mobile=user_model.mobile,
            username=user_model.username,
            isactivated=user_model.isactivated,
            isblocked=user_model.isblocked,
            mailtoken=user_model.mailtoken,
            userpic=user_model.userpic,
            qrcodeurl=user_model.qrcodeurl
        )

# ==========REQUEST================
# query GetUserId($id: ID!) {
#   user(id: $id) {    
#   	id
#     firstname
#     lastname
#     email
#     mobile
#     userpic
#     isactivated
#     isblocked
#     mailtoken
#     userpic
#     qrcodeurl
#   }
# }


# ========VARIABLES======
# {
#   "id": 1
# }