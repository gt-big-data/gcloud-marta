from flask import Blueprint
from sqlalchemy import create_engine
from flask_sqlalchemy import declarative_base

engine = create_engine('sqlite:///gtbigdata:@127.0.0.1:3306/', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

recent_stops = Blueprint("recent-stops", "recent-stops", url_prefix="/recent-stops")

@recent_stops.route("/")
def all_stops():
    return str(list(Base.metadata.tables.keys()))

@recent_stops.route("/<path:path>")
def some_stop():
    return "Not implemented"