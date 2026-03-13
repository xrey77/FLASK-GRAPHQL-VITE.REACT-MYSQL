import strawberry
from flask import Flask
from app.config import db
from flask_sqlalchemy import SQLAlchemy
from strawberry.flask.views import GraphQLView
from strawberry.schema.config import StrawberryConfig
from typing import List 

from app.graphql.types.saleType import SaleType
from app.graphql.types.roleType import RoleType

from app.graphql.queries.user_query import UserQuery
from app.graphql.queries.getuserid_query import GetUserId
from app.graphql.queries.product_query import ProductQuery

from app.graphql.mutations.register.register_mutation import RegisterUser
from app.graphql.mutations.login.userlogin_mutation import LoginUser

from app.models.user import User
from app.models.product import Product
from app.models.sale import Sale
from app.models.role import Role

# db.configure_mappers()                 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rey:rey@127.0.0.1/flask_graphql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# db = SQLAlchemy(app)

@strawberry.type
class Query(UserQuery, GetUserId, ProductQuery):
    pass

@strawberry.type
class Mutation(RegisterUser, LoginUser):
    pass

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=False)
)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)


