from db import db


class StatusModel(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(12))  # new, planned, in_progress, completed

    def __init__(self, name):
        self.name = name
