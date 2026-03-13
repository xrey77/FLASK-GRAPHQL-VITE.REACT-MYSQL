import strawberry
from strawberry.types import Info
from strawberry.flask.views import GraphQLView
from flask import Flask
from sqlalchemy import select
from graphql import GraphQLError

from app.models.user import User, db

from app.graphql.mutations.register.inputs import CreateUserInput
from app.models.user import User
from app.services.hashing import Hasher

@strawberry.type
class CreateUserResponse:
    message: str

@strawberry.type
class RegisterUser:
    @strawberry.mutation
    def create_user(self, input: CreateUserInput) -> CreateUserResponse:
        
        query_email = select(User).where(User.email == input.email)
        result = db.session.execute(query_email)
        if result.scalars().first():
            raise GraphQLError("Email Address is already taken.", extensions={"code": "EMAIL_ALREADY_EXISTS"})

        query_username = select(User).where(User.username == input.username)
        result = db.session.execute(query_username)
        if result.scalars().first():
            raise GraphQLError("Username is already taken.", extensions={"code": "USERNAME_ALREADY_EXISTS"})

        new_user = User(
            firstname=input.firstname,
            lastname=input.lastname,
            email=input.email,
            mobile=input.mobile,
            username=input.username,
            password=Hasher.get_password_hash(input.password),
            role_id=2
        )
        
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)

        return CreateUserResponse(message="You have registered successfully, please login now.")

# ========REQUEST===============
# mutation CreateUser($input: CreateUserInput!) {
#   create_user(input: $input) {
#     message
#   }
# }


# =========VARIABLES==========
# {
#   "input": {
#     "firstname": "Rey",
#     "lastname": "Gragasin",
#     "email": "rey@yahoo.com",
#     "mobile": "12345890",
#     "username": "Rey",
#     "password": "rey"
#   }
# }
