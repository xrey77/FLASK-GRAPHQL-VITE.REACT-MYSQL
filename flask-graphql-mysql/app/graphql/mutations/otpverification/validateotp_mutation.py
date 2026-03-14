import strawberry
from graphql import GraphQLError
from app.models.user import User, db
from app.graphql.mutations.otpverification.inputs import OtpInput
import pyotp

@strawberry.type
class OtpResponse:
    message: str
    username: str

@strawberry.type
class VerifyOtp:
    @strawberry.mutation
    def verify_otp(self, input: OtpInput) -> OtpResponse:
        user_id = input.id
        
        user_model = db.session.get(User, user_id) 
        
        if not user_model:
            raise GraphQLError("User ID Not found.", extensions={"code": "USER_ID_NOT_FOUND"})

        if user_model.secret is None: 
            raise GraphQLError("Multi-Factor is not yer enabled.", extensions={"code": "MFA_IS_NOT_YET_ENABLED"})

        if input.otp is not None:
            if pyotp.TOTP(user_model.secret).verify(input.otp):
                return OtpResponse(
                    message="OTP validation successfull.",
                    username=user_model.username)
            else:
                raise GraphQLError("Invalid OTP code, please try again.", extensions={"code": "INVALID_OTP_TRYAGAIN"})
        

# ========REQUEST===============
# mutation VerifyOtp($input: OtpInput!) {
#   verify_otp(input: $input) {
#     message
#     username
#   }
# }


# =========VARIABLES==========
# {
#   "input": {
#     "id": 1,
#     "otp": "12345890",
#   }
# }
