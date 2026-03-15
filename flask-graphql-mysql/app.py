import strawberry
from flask_cors import CORS
import os
from flask import Flask, render_template, request

from app.config import db
from flask_sqlalchemy import SQLAlchemy
from strawberry.flask.views import GraphQLView
from app.services.authGraphql_view import XGraphQLView


from strawberry.schema.config import StrawberryConfig
from typing import List 
from app.services.auth import JWT_SECRET_KEY
from app.services.auth import decode_token

from app.graphql.types.saleType import SaleType
from app.graphql.types.roleType import RoleType

from app.graphql.queries.user_query import UserQuery
from app.graphql.queries.getuserid_query import GetUserId
from app.graphql.queries.product_query import ProductQuery
from app.graphql.queries.sales_query import SaleQuery
from app.graphql.queries.list_query import ProductList
from app.graphql.queries.search_query import ProductSearch
from app.graphql.queries.productcategory_query import CategoryQuery

from app.graphql.mutations.register.register_mutation import RegisterUser
from app.graphql.mutations.login.userlogin_mutation import LoginUser
from app.graphql.mutations.updateprofile.profile_mutation import UpdateProfile
from app.graphql.mutations.updatepassword.updatepassword_mutation import ChangePassword
from app.graphql.mutations.activatemfa.mfaactivation_mutation import ActivateMfa
from app.graphql.mutations.uploaduserpic.uploadprofilepic_mutation import UploadPicture
from app.graphql.mutations.otpverification.validateotp_mutation import VerifyOtp

from app.models.user import User
from app.models.product import Product
from app.models.sale import Sale
from app.models.role import Role
from app.models.category import Category

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rey:rey@127.0.0.1/flask_graphql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
@strawberry.type
class Query(UserQuery, GetUserId, ProductQuery, SaleQuery, ProductList, ProductSearch, CategoryQuery):
    pass

@strawberry.type
class Mutation(RegisterUser, LoginUser, UpdateProfile, ChangePassword, ActivateMfa, UploadPicture, VerifyOtp):
    pass

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=False)
)

CORS(app, resources={r"/graphql": {"origins": "http://localhost:5173"}})

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/images')
def gallery():
    image_names = os.listdir('static/images')
    return render_template(image_names=image_names)

@app.route('/products')
def product_gallery():
    image_names = os.listdir('static/products') 
    return render_template(image_names=image_names, folder='products')

@app.route('/users')
def users():
    image_names = os.listdir('static/users')
    return render_template(image_names=image_names)

app.add_url_rule(
    "/graphql",
    view_func=XGraphQLView.as_view(
        "graphql_view", 
        schema=schema, 
        multipart_uploads_enabled=True
    ),
)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)


