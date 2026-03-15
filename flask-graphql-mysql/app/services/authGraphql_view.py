from strawberry.flask.views import GraphQLView
from flask import Request, Response, session
from app.services.auth import decode_token
from app.models.user import User, db
from graphql import GraphQLError
from sqlalchemy.future import select

class XGraphQLView(GraphQLView):
    def get_context(self, request: Request, response: Response): 
        auth_header = request.headers.get("Authorization")
        user = None
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            try:
                payload = decode_token(token)
                user_id = payload.get("sub")
                result = db.session.execute(select(User).where(User.email == user_id))
                user = result.scalars().first()
            except Exception as e:
                raise GraphQLError(f"Token Error, " + e)                

        print(f"Current User in Context: {user}")

        return {
            "request": request,
            "response": response,
            "user": user
        }