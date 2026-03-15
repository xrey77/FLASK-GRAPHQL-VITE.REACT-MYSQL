import strawberry
from strawberry.types import Info
from graphql import GraphQLError
from app.models.user import User, db
from app.graphql.mutations.updateprofile.inputs import UserProfileInput
from app.services.isAuthenticated import IsAuthenticated

@strawberry.type
class ProfileResponse:
    message: str

@strawberry.type
class UpdateProfile:

    @strawberry.field(permission_classes=[IsAuthenticated])    
    def update_profile(self, info: Info, input: UserProfileInput) -> ProfileResponse:
        user_id = input.id
        
        user_model = db.session.get(User, user_id) 
        
        if not user_model:
            raise GraphQLError("User ID Not found.", extensions={"code": "USER_ID_NOT_FOUND"})

        if input.firstname is not strawberry.UNSET:
            user_model.firstname = input.firstname
        if input.lastname is not strawberry.UNSET:
            user_model.lastname = input.lastname
        if input.mobile is not strawberry.UNSET:
            user_model.mobile = input.mobile
        
        try:
            db.session.commit()
            return ProfileResponse(message="You have updated your profile successfully.")
        except Exception as e:
            db.session.rollback()
            raise GraphQLError(f"Update failed: {str(e)}")


# ========REQUEST===============
# mutation UpdateProfile($input: UserProfileInput!) {
#   update_profile(input: $input) {
#     message
#   }
# }


# =========VARIABLES==========
# {
#   "input": {
#     "id": 1,
#     "firstname": "Rey",
#     "lastname": "Gragasin",
#     "mobile": "12345890",
#   }
# }
