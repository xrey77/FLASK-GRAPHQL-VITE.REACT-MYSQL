import strawberry

@strawberry.input
class PasswordInput:
    id: int
    password: str



