import datetime
from db import db
from .status import StatusModel


class CaseHistoryModel(db.Model):
    __tablename__ = 'case_history'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id', ondelete='CASCADE'))
    time_date = db.Column(db.DateTime, default=datetime.datetime.now())
    operation = db.Column(db.Text)

    case = db.relationship('CaseModel')

    def __init__(self, operation, case_id):
        self.operation = operation
        self.case_id = case_id

    def json(self):
        return {
            'time_date': str(self.time_date),
            'operation': self.operation
        }

    def save_to_db(self):
        db.session.add(self)

    @staticmethod
    def commit_changes():
        db.session.commit()

    @classmethod
    def find_all_by_case_id(cls, case_id):
        return cls.query.filter_by(case_id=case_id).all()
