# from db import db
#
#
# class StatusModel(db.Model):
#     __tablename__ = 'status'
#
#     id = db.Column(db.Integer, primary_key=True)
#     status_name = db.Column(db.String(12))  # new, planned, in_progress, completed
#
#     def __init__(self, status_name):
#         self.status_name = status_name
