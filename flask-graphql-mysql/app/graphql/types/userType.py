import strawberry
from typing import Optional
from decimal import Decimal
from typing import Optional, List, Annotated
from app.graphql.types.roleType import RoleType

@strawberry.type
class UserType:
    id: strawberry.ID
    firstname: str
    lastname: str
    email: str
    username: str
    # Fields with defaults
    mobile: Optional[str] = None
    isactivated: int = 1
    isblocked: int = 0
    mailtoken: int = 0
    userpic: str = "pix.png"
    secret: Optional[str] = None
    qrcodeurl: Optional[str] = None
    role_id: Optional[int] = None
    role: Optional[RoleType] = None
