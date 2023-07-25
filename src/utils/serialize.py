import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal) or (
            not type(obj) in [int, float, complex, dict, tuple, list, bool]
            and obj is not None
        ):
            return str(obj)


def serialize(obj):
    """Serialize an object into JSON."""
    try:
        return json.dumps(obj, indent=4, cls=DecimalEncoder)
    except TypeError:
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
