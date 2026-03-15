import strawberry
import os
from graphql import GraphQLError
from app.models.user import User, db
from app.graphql.mutations.uploaduserpic.inputs import UploadInput
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import current_app
from app.services.isAuthenticated import IsAuthenticated

@strawberry.type
class UploadResponse:
    message: str
    userpic: str

@strawberry.type
class UploadPicture:

    @strawberry.field(permission_classes=[IsAuthenticated])    
    def upload_picture(self, input: "UploadInput") -> UploadResponse:
        user_id = str(input.id)
        file = input.file
        
        user_model = db.session.get(User, user_id) 
        if not user_model:
            raise GraphQLError("User ID Not found.", extensions={"code": "USER_ID_NOT_FOUND"})

        filename = secure_filename(file.filename)
        extension = Path(filename).suffix
        newfilename = "00" + user_id + extension;
        upload_path = os.path.join(current_app.root_path, 'static', 'users', newfilename)
        
        try:
            file.save(upload_path) 
        except Exception as e:
            raise GraphQLError(f"File save failed: {str(e)}")

        user_model.userpic = newfilename

        try:
            db.session.commit()
            return UploadResponse(
                message="You have changed your profile picture successfully.",
                userpic=newfilename)
        except Exception as e:
            db.session.rollback()
            raise GraphQLError(f"Update failed: {str(e)}")

# ======REQUEST=======
# mutation UploadPicture($input: UploadInput!) {
#     upload_picture(input: $input) {
#         message
#         userpic
#     }
# }

# =======VARIABLES======
# {
#     "input": {
#         "id": 1
#         "file": null
#     }
# }