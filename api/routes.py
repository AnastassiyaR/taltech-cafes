from flask import jsonify, request, abort, Blueprint
from api.data import load_data, save_data, next_id
from api.helpers import is_open_during, validate_time, validate_provider_field, validate_text_field


api = Blueprint("api", __name__)


@api.route("/api/cafes", methods=["GET"])
def get_all():
    return jsonify(load_data())


@api.route("/api/cafes/open", methods=["GET"])
def get_by_time():
    from_time = request.args.get("from")
    to_time = request.args.get("to")
    if not from_time or not to_time:
        abort(400, description="Parameters 'from' and 'to' are required (HH:MM).")
    try:
        result = [c for c in load_data() if is_open_during(c, from_time, to_time)]
    except ValueError:
        abort(400, description="Invalid time format. Use HH:MM.")
    return jsonify(result)


@api.route("/api/cafes/<int:cafe_id>", methods=["GET"])
def get_one(cafe_id):
    cafes = load_data()
    cafe = next((c for c in cafes if c["id"] == cafe_id), None)
    if cafe is None:
        abort(404, description=f"Cafe with ID {cafe_id} not found.")
    return jsonify(cafe)


def _validate_payload(data):
    for field in ("name", "location"):
        if field in data and not validate_text_field(data[field]):
            return f"'{field.capitalize()}' must not be empty or consist only of numbers."
    if "provider" in data and not validate_provider_field(data["provider"]):
        return "Provider must not contain numbers."
    for field in ("time_open", "time_closed"):
        if field in data and not validate_time(data[field]):
            return f"Invalid time format for '{field}': use HH:MM (e.g. 08:30)."
    return None


@api.route("/api/cafes", methods=["POST"])
def add_cafe():
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, description="Invalid JSON.")
    required = ["name", "location", "provider", "time_open", "time_closed"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        abort(400, description=f"Missing fields: {', '.join(missing)}")
    err = _validate_payload(data)
    if err:
        abort(400, description=err)
    cafes = load_data()
    if any(c["name"].lower() == data["name"].strip().lower() for c in cafes):
        abort(400, description=f"A cafe named '{data['name'].strip()}' already exists.")
    new_cafe = {
        "id": next_id(cafes),
        "name": data["name"],
        "location": data["location"],
        "provider": data["provider"],
        "time_open": data["time_open"],
        "time_closed": data["time_closed"],
    }
    cafes.append(new_cafe)
    save_data(cafes)
    return jsonify(new_cafe), 201


@api.route("/api/cafes/<int:cafe_id>", methods=["PUT"])
def update_cafe(cafe_id):
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, description="Invalid JSON.")
    cafes = load_data()
    cafe = next((c for c in cafes if c["id"] == cafe_id), None)
    if cafe is None:
        abort(404, description=f"Cafe with ID {cafe_id} not found.")
    err = _validate_payload(data)
    if err:
        abort(400, description=err)
    if "name" in data:
        new_name = data["name"].strip().lower()
        if any(c["name"].lower() == new_name and c["id"] != cafe_id for c in cafes):
            abort(400, description=f"A cafe named '{data['name'].strip()}' already exists.")
    for field in ("name", "location", "provider", "time_open", "time_closed"):
        if field in data:
            cafe[field] = data[field]
    save_data(cafes)
    return jsonify(cafe)


@api.route("/api/cafes/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    cafes = load_data()
    new_list = [c for c in cafes if c["id"] != cafe_id]
    if len(new_list) == len(cafes):
        abort(404, description=f"Cafe with ID {cafe_id} not found.")
    save_data(new_list)
    return jsonify({"message": f"Cafe {cafe_id} deleted successfully."}), 200
