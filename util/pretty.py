import json, sys

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)