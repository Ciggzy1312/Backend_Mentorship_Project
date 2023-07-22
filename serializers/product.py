from bson import ObjectId

def products_serializer(products) -> dict:
    res = []
    for product in products:
        res.append({
            'id': str(ObjectId(product["_id"])),
            'name': product["name"],
            'description': product["description"],
            'price': product["price"],
            'quantity': product["quantity"],
            'created_by': product["created_by"]
        })

    return res