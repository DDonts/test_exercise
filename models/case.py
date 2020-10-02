import datetime
from db import db
from .status import StatusModel


class CaseModel(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text(256))
    start_time = db.Column(db.DateTime, default=datetime.datetime.now())
    end_time = db.Column(db.DateTime)

    history = db.relationship('CaseHistoryModel', cascade="all,delete")
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'))
    status = db.relationship('StatusModel')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, description, end_time, user_id):
        self.name = name
        self.description = description
        self.end_time = end_time
        self.user_id = user_id
        self.status = StatusModel.query.filter_by(name='New').first()

    def json(self):
        return {
            'name': self.name,
            'description': self.description,
            'start_time': str(self.start_time.strftime('%H:%M:%S %d.%m.%Y')),
            'end_time': str(self.end_time.strftime('%H:%M:%S %d.%m.%Y')),
            'status': self.status.name,
            'user_id': self.user_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name_and_user_id(cls, name, user_id):
        return cls.query.filter_by(name=name, user_id=user_id).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all_by_user_id(cls, user_id, status="%%", end_time="%%"):
        return cls.query.filter((CaseModel.user_id == user_id) &
                                (CaseModel.status_id.like(status)) &
                                (CaseModel.end_time.like(end_time))).all()
