from flask import Blueprint

recent_stops = Blueprint("recent-stops", "recent-stops", url_prefix="/recent-stops")

@recent_stops.route("/")
def all_stops():
    return "Not implemented"

@recent_stops.route("/<path:path>")
def some_stop():
    return "Not implemented"