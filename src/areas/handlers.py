from flask_restful import Resource
from .service import AreasService
from helpers.responses import success_response, error_response

class Areas(Resource):
    def __init__(self, service: AreasService):
        self.service = service

    def get(self):
        areas = self.service.fetch_all_areas()
        return success_response(areas)

class AreaDetail(Resource):
    def __init__(self, service: AreasService):
        self.service = service

    def get(self, area_id):
        area_details = self.service.fetch_area_details(area_id)
        if area_details is None:
            return error_response("Area not found", 404)
        return success_response(area_details)
