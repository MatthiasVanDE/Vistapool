"""Hulpmethode om Firestore JSON te parsen naar een normale Python-dict."""

def parse_firestore_doc(doc_json):
    """Parse Firestore doc (mapValue, fields, etc.) naar gewone dict."""
    if not doc_json or "fields" not in doc_json:
        return {}
    return _parse_value({"mapValue": {"fields": doc_json["fields"]}})

def _parse_value(value):
    if "mapValue" in value:
        return _parse_map_value(value["mapValue"])
    if "arrayValue" in value:
        return _parse_array_value(value["arrayValue"])
    if "stringValue" in value:
        return value["stringValue"]
    if "integerValue" in value:
        return int(value["integerValue"])
    if "doubleValue" in value:
        return float(value["doubleValue"])
    if "booleanValue" in value:
        return bool(value["booleanValue"])
    if "nullValue" in value:
        return None
    return None  # fallback

def _parse_map_value(map_val):
    fields = map_val.get("fields", {})
    result = {}
    for k, v in fields.items():
        result[k] = _parse_value(v)
    return result

def _parse_array_value(arr_val):
    values = arr_val.get("values", [])
    return [_parse_value(v) for v in values]
