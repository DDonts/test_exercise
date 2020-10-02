from datetime import datetime

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.case import CaseModel
from models.case_history import CaseHistoryModel

statuses = {
    'New': 1,
    'Planned': 2,
    'In progress': 3,
    'Completed': 4
}


def logging_of_editing(field: str, old: str, new: str, case_id: int):
    operation = field + ": '" + old + "' -> '" + new + "'."
    new_log = CaseHistoryModel(operation, case_id)
    new_log.save_to_db()


class Case(Resource):
    @jwt_required
    def get(self):
        """
        URL: http://{{server_url}}/case
        METHOD: GET

        Headers: Authorization - "Bearer {{access_token}}"
        Input: {
            "status": "new/planned/in_progress/completed"   (optional)
            "end_time": "Hour:Minutes Day.Month.Year"       (optional)
        }
        :return: List of cases
        """
        data = request.get_json()
        try:
            user = get_jwt_identity()
            if not data:
                data = {}
            if "end_time" not in data:
                data['end_time'] = "%%"
            else:
                try:
                    data['end_time'] = str(datetime.strptime(data['end_time'], '%H:%M:%S %d.%m.%Y'))
                except:
                    return {'message': 'Incorrect datetime format'}, 400
            if "status" not in data:
                data['status'] = "%%"
            cases = [case.json() for case in CaseModel.find_all_by_user_id(user, data['status'], data['end_time'])]
            return {'cases': cases}, 200
        except:
            return {'message': 'Internal server error'}, 500

    @jwt_required
    def post(self):
        """
        URL: http://{{server_url}}/case
        METHOD: POST

        Headers:
            Content-Type: application/json
            Authorization: "Bearer {{access_token}}"

        Input: {
            "name": "name of the required case",
            "description": "some description"
            "end_time": "Hour:Minutes Day.Month.Year",
        }
        :return: JSON of created case.
        """
        data = request.get_json()
        try:
            user = get_jwt_identity()
            if len(data['name']) > 30:
                return {'message': "Name is too long. Max length is 30 symbols"}, 400
            if CaseModel.find_by_name_and_user_id(data['name'], user):
                return {'message': "An case with name '{}' already exists.".format(data['name'])}, 400
            if len(data['description']) > 256:
                return {'message': "Description is too long. Max length is 256 symbols"}, 400

            try:
                end_time = datetime.strptime(data['end_time'], '%H:%M:%S %d.%m.%Y')
            except:
                return {'message': 'Incorrect datetime format'}, 400

            if end_time < datetime.now():
                return {'message': "This end_time has passed."}
            else:
                data['end_time'] = str(end_time)
            case = CaseModel(**data, user_id=user)

            try:
                case.save_to_db()
            except:
                return {"message": "An error occurred inserting the case."}, 500
            logging_of_editing('Creating', '', '', case.id)
        except:
            return {'message': 'Internal server error'}, 500
        return case.json(), 201

    @jwt_required
    def delete(self):
        """
        URL: http://{{server_url}}/case
        METHOD: DELETE

        Headers:
            Content-Type: application/json
            Authorization: "Bearer {{access_token}}"

        Input: {
            "name": "name of the required case"
        }
        :return: JSON of report message
        """
        data = request.get_json()
        try:
            user = get_jwt_identity()
            case = CaseModel.find_by_name_and_user_id(data['name'], user)
            if case:
                case.delete_from_db()
                return {'message': 'Case deleted.'}
            return {'message': 'Case not found.'}, 404
        except:
            return {'message': 'Internal server error'}, 500

    @jwt_required
    def put(self):
        """
        URL: http://{{server_url}}/case
        METHOD: PUT

        Updates received fields and logging changes to case_history table

        Headers:
            Content-Type: application/json
            Authorization: "Bearer {{access_token}}"

        Input: {
            "name": "name of the required case",
            "new_name": "new name of the case"               (optional)
            "new_description": "some new some description"   (optional)
            "new_status": "new/planned/in_progress/completed",   (optional)
            "new_end_time": "Hour:Minutes Day.Month.Year",       (optional)
        }
        :return: JSON of edited case
        """
        data = request.get_json()
        try:
            user = get_jwt_identity()
            case = CaseModel.find_by_name_and_user_id(data['name'], user)
            if case:
                if 'new_name' in data:
                    if CaseModel.find_by_name_and_user_id(data['new_name'], user):
                        return {'message': "An case with name '{}' already exists.".format(data['new_name'])}, 400
                    if len(data['new_name']) > 30:
                        return {'message': "New name is too long. Max length is 30 symbols"}, 400
                    if case.name != data['new_name']:
                        logging_of_editing(field='Name', old=case.name, new=data['new_name'], case_id=case.id)
                        case.name = data['new_name']

                if 'new_description' in data:
                    if len(data['new_description']) > 256:
                        return {'message': "New description is too long. Max length is 256 symbols"}, 400
                    if case.description != data['new_description']:
                        logging_of_editing(field='Description', old=case.description, new=data['new_description'],
                                           case_id=case.id)
                        case.description = data['new_description']

                if 'new_status' in data:
                    if data['new_status'] in statuses:
                        if case.status_id != statuses[data['new_status']]:
                            logging_of_editing(field='Status', old=case.status.name, new=data['new_status'],
                                               case_id=case.id)
                            case.status_id = statuses[data['new_status']]
                    else:
                        return {'message': "Wrong status format. "
                                           "Available statuses: New, Planned, In progress, Completed"}, 400

                if 'new_end_time' in data:
                    try:
                        new_end_time = datetime.strptime(data['new_end_time'], '%H:%M:%S %d.%m.%Y')
                    except:
                        return {'message': 'Incorrect datetime format'}, 400
                    if new_end_time < case.start_time:
                        return {'message': "This new end_time has passed."}
                    else:
                        if str(case.end_time) != str(new_end_time):
                            logging_of_editing(field='end_time', old=str(case.end_time), new=str(new_end_time),
                                               case_id=case.id)
                            case.end_time = str(new_end_time)

            else:
                return {'message': 'Case not found.'}, 404
            try:
                case.save_to_db()
            except:
                return {"message": "An error occurred updating the case."}, 500
        except:
            return {'message': 'Internal server error'}, 500
        return case.json()


class CaseHistory(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        """
        URL: http://{{server_url}}/case_history
        METHOD: POST

        Headers:
            Content-Type: application/json
            Authorization: "Bearer {{access_token}}"

        Input: {
            "name": "name of the required case"
        }
        :return: JSON of history of case.
        """
        data = request.get_json()
        try:
            user = get_jwt_identity()
            case = CaseModel.find_by_name_and_user_id(data['name'], user)
            case_id = case.id
            if case:
                case_history = [history.json() for history in CaseHistoryModel.find_all_by_case_id(case_id)]
                return {'history': case_history}, 200
            else:
                return {'message': 'Case not found'}, 404
        except:
            return {'message': 'Internal server error'}, 500
