from bson import ObjectId

def basket_serializer(basket) -> dict:
    return {
        'userId': str(basket["userId"]),
        'products': basket["products"]
    }