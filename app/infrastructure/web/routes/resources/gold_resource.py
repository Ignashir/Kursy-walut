from pathlib import Path
from datetime import datetime
from flask import request, jsonify, send_file
from flask_restful import Resource

from app.domain.service import GoldService
from app.domain.event import WebRequestEvent
from app.infrastructure.observer.configuration import event


class GoldResource(Resource):
    def get(self):
        request_data = dict(request.args)
        if request_data.get('graph'):
            request_data.pop('graph')
            GoldService().pull_gold_from_api(**request_data).draw_graph()
            event.publish(WebRequestEvent(request.method, 200, datetime.today()))
            return send_file(Path.cwd().joinpath("app/infrastructure/web/static_resources/gold-plot.png"), mimetype='image/png')
        event.publish(WebRequestEvent(request.method, 200, datetime.today()))
        return jsonify({'result': GoldService().pull_gold_from_api(**request_data).get_gold()})
