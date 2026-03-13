import strawberry
from graphql import GraphQLError
from sqlalchemy.future import select

from app.models.user import User, db
from app.graphql.types.userType import UserType
from app.graphql.types.roleType import RoleType
from app.graphql.mutations.login.inputs import LoginInput
from app.services.hashing import Hasher
from app.services.auth import create_access_token


@strawberry.type
class LoginResponse:
    message: str
    token: str
    user: UserType

@strawberry.type
class LoginUser:
    @strawberry.mutation
    def login(self, input: LoginInput) -> LoginResponse:
        result = db.session.execute(select(User).where(User.username == input.username))
        user = result.scalars().first()

        if not user:
            raise GraphQLError(
                "Username not found, please try again.",
                extensions={"code": "USERNAME_NOT_FOUND"}
            )

        if not Hasher.verify_password(input.password, user.password):
            raise GraphQLError(
                "Invalid Password, please try again.",
                extensions={"code": "INVALID_PASSWORD_PLEASE_TRY_AGAIN"}
            )

        token = create_access_token(data={"sub": user.email})
        
        user_data = UserType(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            mobile=user.mobile,
            username=user.username,
            isactivated= user.isactivated,
            isblocked=user.isblocked,
            mailtoken=user.mailtoken,
            userpic=user.userpic,
            secret=user.secret,
            qrcodeurl=user.qrcodeurl,
            role_id=user.role_id,
            role=RoleType(id=str(user.role.id), name=user.role.name) if user.role else None
        )

        return LoginResponse(
            message="You have logged-in successfully, please wait.",
            token=token,
            user=user_data
        )

# ==========REQUEST==============
# mutation LoginUser($input: LoginInput!) {  
#   login(input: $input) {
#     message
#     token
#     user {
#       id
#       firstname
#       lastname
#       email
#       mobile      
#       username
#       isactivated
#       isblocked
#       mailtoken      
#       userpic
#       qrcodeurl
#     }
#   }
# }


# ==========VARIABLES=======
# {
#   "input": {
#     "username": "Rey",
#     "password": "rey"
#   }
# }
