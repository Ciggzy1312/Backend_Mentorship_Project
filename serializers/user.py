from bson import ObjectId

def user_serializer(user) -> dict:
    return {
        'id': str(ObjectId(user["_id"])),
        'name': user["name"],
        'email': user["email"]
    }