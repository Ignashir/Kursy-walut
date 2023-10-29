from flask import request
from flask_restful import Resource

from app.domain.service import GoldService


class GoldResource(Resource):
    def get(self):
        return {'result': GoldService().pull_gold_from_api(**request.args).get_gold()}

    # TODO to samo co w currency czyli dodac mozliwosc wysylania wykresu
    