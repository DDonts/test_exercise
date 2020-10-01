from datetime import datetime

from flask_restful import Resource
from flask import request
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity,
                                fresh_jwt_required)
from models.case import CaseModel


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
        user = get_jwt_identity()
        data = request.get_json()
        if not data:
            data = {}
        if "end_time" not in data:
            data['end_time'] = "%%"
        else:
            data['end_time'] = str(datetime.strptime(data['end_time'], '%H:%M %d.%m.%Y'))
        if "status" not in data:
            data['status'] = "%%"
        cases = [case.json() for case in CaseModel.find_all_by_user_id(user, data['status'], data['end_time'])]
        return {'cases': cases}, 200

    @fresh_jwt_required
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
        user = get_jwt_identity()
        data = request.get_json()
        if len(data['name']) > 30:
            return {'message': "Name is too long. Max length is 30 symbols"}, 400
        if len(data['description']) > 256:
            return {'message': "Description is too long. Max length is 256 symbols"}, 400
        if CaseModel.find_by_name_and_user_id(data['name'], user):
            return {'message': "An case with name '{}' already exists.".format(data['name'])}, 400

        data['end_time'] = str(datetime.strptime(data['end_time'], '%H:%M %d.%m.%Y'))

        case = CaseModel(**data, user_id=user)

        try:
            case.save_to_db()
        except:
            return {"message": "An error occurred inserting the case."}, 500

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
        user = get_jwt_identity()
        data = request.get_json()

        case = CaseModel.find_by_name_and_user_id(data['name'], user)
        if case:
            case.delete_from_db()
            return {'message': 'Case deleted.'}
        return {'message': 'Case not found.'}, 404

    @jwt_required
    def put(self):
        """
        URL: http://{{server_url}}/case
        METHOD: PUT

        Headers:
            Content-Type: application/json
            Authorization: "Bearer {{access_token}}"

        Input: {
            "name": "name of the required case",
            "new_name": "new name of the case"               (optional)
            "new_description": "some new some description"   (optional)
            "status": "new/planned/in_progress/completed",   (optional)
            "end_time": "Hour:Minutes Day.Month.Year",       (optional)
        }
        :return: JSON of edited case
        """
        user = get_jwt_identity()
        data = request.get_json()
        case = CaseModel.find_by_name_and_user_id(data['name'], user)

        if case:
            if 'new_name' in data:
                if CaseModel.find_by_name_and_user_id(data['new_name'], user):
                    return {'message': "An case with name '{}' already exists.".format(data['new_name'])}, 400
                if len(data['new_name']) > 30:
                    return {'message': "New name is too long. Max length is 30 symbols"}, 400
                case.name = data['new_name']
            if 'new_description' in data:
                if len(data['description']) > 256:
                    return {'message': "New description is too long. Max length is 256 symbols"}, 400
                case.description = data['new_description']
            if 'new_status' in data:
                case.status = data['new_status']
            if 'new_end_time' in data:
                case.end_time = str(datetime.strptime(data['new_end_time'], '%H:%M %d.%m.%Y'))
        else:
            return {'message': 'Case not found.'}, 404
        case.save_to_db()

        return case.json()
