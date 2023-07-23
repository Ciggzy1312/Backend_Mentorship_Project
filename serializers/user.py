from bson import ObjectId

def user_serializer(user) -> dict:
    return {
        'id': str(ObjectId(user["_id"])),
        'name': user["name"],
        'email': user["email"],
        'address': {
                    'addStreet1': user["address"]["addStreet1"],
                    'addrStreet2': user["address"]["addrStreet2"],
                    'city': user["address"]["city"],
                    'state': user["address"]["state"],
                    'country': user["address"]["country"],
                    'zip': user["address"]["zip"]
                    }
        }