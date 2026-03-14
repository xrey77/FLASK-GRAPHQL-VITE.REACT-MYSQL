import strawberry
import pyotp
import qrcode
import base64
import io
from typing import Optional 
from strawberry.types import Info
from strawberry.flask.views import GraphQLView
from flask import Flask
from sqlalchemy import select
from graphql import GraphQLError
from app.models.user import User, db
from app.graphql.mutations.activatemfa.inputs import MfaActivationInput
from app.models.user import User

@strawberry.type
class MfaActivationResponse:
    message: str
    qrcodeurl: Optional[str] 

@strawberry.type
class ActivateMfa:
    @strawberry.mutation
    def activate_mfa(self, input: MfaActivationInput) -> MfaActivationResponse:
        # 1. Fetch the user
        user_model = db.session.get(User, input.id)         
        if not user_model:
            raise GraphQLError("User ID Not found.", extensions={"code": "USER_ID_NOT_FOUND"})

        if input.twofactorenabled:
            # 2. Generate TOTP Secret and URI
            secret = pyotp.random_base32()
            uri = pyotp.totp.TOTP(secret).provisioning_uri(
                name=user_model.email, 
                issuer_name="BARCLAYS BANK"
            )            

            # 3. Generate QR Code as Base64 string
            img = qrcode.make(uri)            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            imgbase64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            b64image = "data:image/png;base64," + imgbase64; 
            user_model.secret = secret
            user_model.qrcodeurl = b64image
            qrcodeurl = b64image
            message = "Multi-Factor Authenticator enabled successfully."
        else:
            user_model.secret = None
            user_model.qrcodeurl = None
            qrcodeurl = None
            message = "Multi-Factor Authenticator disabled successfully."

        try:
            db.session.commit()
            return MfaActivationResponse(message=message, qrcodeurl=qrcodeurl)
        except Exception as e:
            db.session.rollback()
            raise GraphQLError(f"Update failed: {str(e)}")



# ========REQUEST===============
# mutation ActivateMfa($input: MfaActivationInput!) {
#   activate_mfa(input: $input) {
#     message
#   }
# }


# =========VARIABLES==========
# {
#   "input": {
#     "id": 1,
#     "twofactorenabled": false
#   }
# }
