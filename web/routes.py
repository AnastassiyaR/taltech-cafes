from flask import Blueprint, render_template, request, redirect, url_for, flash
from api.data import load_data, save_data, next_id
from api.helpers import is_open_during, validate_time, validate_provider_field, validate_text_field


web = Blueprint("web", __name__)


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


@web.route("/")
def index():
    return render_template("index.html", cafes=load_data())


@web.route("/search", methods=["GET", "POST"])
def search():
    results = None
    from_time = ""
    to_time = ""
    error = None

    if request.method == "POST":
        from_time = request.form.get("from_time", "").strip()
        to_time = request.form.get("to_time", "").strip()
        if not from_time or not to_time:
            error = "Please enter both times."
        else:
            try:
                results = [c for c in load_data() if is_open_during(c, from_time, to_time)]
            except ValueError:
                error = "Invalid time format. Use HH:MM."

    return render_template("search.html", results=results,
                           from_time=from_time, to_time=to_time, error=error)


@web.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        payload = {
            "name": request.form["name"].strip(),
            "location": request.form["location"].strip(),
            "provider": request.form["provider"].strip(),
            "time_open": request.form["time_open"].strip(),
            "time_closed": request.form["time_closed"].strip(),
        }
        err = _validate_payload(payload)
        cafes = load_data()
        if err:
            flash(err, "danger")
        elif any(c["name"].lower() == payload["name"].lower() for c in cafes):
            flash(f"A cafe named '{payload['name']}' already exists.", "danger")
        else:
            cafes.append({"id": next_id(cafes), **payload})
            save_data(cafes)
            flash("Cafe added successfully!", "success")
            return redirect(url_for("web.index"))

    return render_template("add.html")


@web.route("/edit/<int:cafe_id>", methods=["GET", "POST"])
def edit(cafe_id):
    cafes = load_data()
    cafe = next((c for c in cafes if c["id"] == cafe_id), None)
    if cafe is None:
        flash("Cafe not found.", "danger")
        return redirect(url_for("web.index"))

    if request.method == "POST":
        payload = {
            "name": request.form["name"].strip(),
            "location": request.form["location"].strip(),
            "provider": request.form["provider"].strip(),
            "time_open": request.form["time_open"].strip(),
            "time_closed": request.form["time_closed"].strip(),
        }
        err = _validate_payload(payload)
        if err:
            flash(err, "danger")
        elif any(c["name"].lower() == payload["name"].lower() and c["id"] != cafe_id for c in cafes):
            flash(f"A cafe named '{payload['name']}' already exists.", "danger")
        else:
            cafe.update(payload)
            save_data(cafes)
            flash("Cafe updated successfully!", "success")
            return redirect(url_for("web.index"))

    return render_template("edit.html", cafe=cafe)


@web.route("/delete/<int:cafe_id>", methods=["POST"])
def delete(cafe_id):
    cafes = load_data()
    new_list = [c for c in cafes if c["id"] != cafe_id]
    if len(new_list) == len(cafes):
        flash("Cafe not found.", "danger")
    else:
        save_data(new_list)
        flash("Cafe deleted successfully.", "success")
    return redirect(url_for("web.index"))
