from pathlib import Path
from datetime import datetime
from flask import request, jsonify, send_file
from flask_restful import Resource

from app.domain.service import GoldService, PredictorService
from app.domain.event import WebRequestEvent, PDFCreateEvent
from app.infrastructure.observer.configuration import event


class GoldResource(Resource):
    @staticmethod
    def get():
        request_data = dict(request.args)
        if request_data.get('graph'):
            request_data.pop('graph')
            GoldService().pull_gold_from_api(**request_data).draw_graph()
            event.publish(WebRequestEvent(request.method, 200, datetime.today()))
            return send_file(Path.cwd().joinpath("app/infrastructure/web/static_resources/gold-plot.png"),
                             mimetype='image/png')
        elif request_data.get('pdf'):
            request_data.pop('pdf')
            GoldService().pull_gold_from_api(**request_data).draw_graph().get_report()
            event.publish(PDFCreateEvent(datetime.today()))
            event.publish(WebRequestEvent(request.method, 200, datetime.today()))
            return send_file(Path.cwd().joinpath("app/infrastructure/web/static_resources/report.pdf"))
        else:
            event.publish(WebRequestEvent(request.method, 200, datetime.today()))
            return jsonify({'result': GoldService().pull_gold_from_api(**request_data).get_gold()})


class GoldPredictor(Resource):
    def get(self, date_to_predict: str):
        return jsonify({f'predicted value for {date_to_predict}': PredictorService().predict_value(date_to_predict)})
