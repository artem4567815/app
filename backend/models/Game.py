from .alchemy import *

db = SQLAlchemy()


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    steam_price = db.Column(db.Float, nullable=True)
    epic_price = db.Column(db.Float, nullable=True)
