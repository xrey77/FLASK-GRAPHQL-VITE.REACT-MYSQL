import strawberry

@strawberry.input
class UserProfileInput:
    id: int
    firstname: str
    lastname: str
    mobile: str



