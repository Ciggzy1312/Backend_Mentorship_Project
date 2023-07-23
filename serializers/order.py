from bson import ObjectId

def order_serializer(order) -> dict:
    return {
        'basketId': str(ObjectId(order["basketId"]))
    }

def orders_serializer(orders) -> dict:
    res = []
    for order in orders:
        res.append({
            'basketId': str(ObjectId(order["basketId"]))
            })

    return res