import strawberry

@strawberry.type
class RoleType:
    id: strawberry.ID
    name: str
