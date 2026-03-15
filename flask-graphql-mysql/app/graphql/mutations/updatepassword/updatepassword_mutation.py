import strawberry
from strawberry.types import Info
from strawberry.flask.views import GraphQLView
from flask import Flask
from sqlalchemy import select
from graphql import GraphQLError
from app.models.user import User, db
from app.graphql.mutations.updatepassword.inputs import PasswordInput
from app.models.user import User
from app.services.hashing import Hasher
from app.services.isAuthenticated import IsAuthenticated

@strawberry.type
class PasswordUpdateResponse:
    message: str

@strawberry.type
class ChangePassword:

    @strawberry.field(permission_classes=[IsAuthenticated])    
    def change_password(self, input: PasswordInput) -> PasswordUpdateResponse:
        user_id = input.id

        user_model = db.session.get(User, user_id) 
        
        if not user_model:
            raise GraphQLError("User ID Not found.", extensions={"code": "USER_ID_NOT_FOUND"})

        if input.password is not strawberry.UNSET:
            user_model.password = Hasher.get_password_hash(input.password)
        
        try:
            db.session.commit()
            return PasswordUpdateResponse(message="You have changed your password successfully.")
        except Exception as e:
            db.session.rollback()
            raise GraphQLError(f"Update failed: {str(e)}")


# ========REQUEST===============
# mutation ChangePassword($input: PasswordInput!) {
#   change_password(input: $input) {
#     message
#   }
# }


# =========VARIABLES==========
# {
#   "input": {
#     "id": 1,
#     "password": "rey"
#   }
# }
