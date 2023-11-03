from flask import jsonify, request, send_file
from pathlib import Path
from datetime import datetime
from app.domain.service import CurrencyService
from app.domain.event import WebRequestEvent
from app.infrastructure.observer.configuration import event


def no_graph(request_data: dict, many_currency: bool = False, code: str | None = None):
    pull = CurrencyService()
    pull.pull_many_currencies_from_api(**request_data) if many_currency else pull.pull_currency_from_api(code, **request_data)
    event.publish(WebRequestEvent(request.method, 200, datetime.today()))
    return jsonify({'result': pull.get_currency()})


def with_graph(request_data: dict, many_currency: bool = False, code: str | None = None):
    pull = CurrencyService()
    pull.pull_many_currencies_from_api(**request_data) if many_currency else pull.pull_currency_from_api(code, **request_data)
    pull.draw_graph(many=many_currency)
    path_to_graph = Path.cwd().joinpath(f"app/infrastructure/web/static_resources/{'many-currency' if many_currency else 'one-currency'}.png")
    event.publish(WebRequestEvent(request.method, 200, datetime.today()))
    return send_file(path_or_file=path_to_graph, mimetype='image/png')


# TODO trzeba sprawdzac czy dzien pobierania jest dniem roboczym
def create_routing(app):
    @app.route('/currency', methods=['GET'])
    def get_all_currencies():
        '''
        Pulling currencies from api with parameters in query
        :return: return pulled currency filtered by query parameters, if graph is True then create a graph based on data and return it
        '''
        graph = False
        request_data = dict(request.args)
        if request_data.get('graph'):
            graph = request_data.pop('graph')
        return with_graph(request_data, True) if graph else no_graph(request_data, True)

    @app.route('/currency/<string:code>', methods=['GET'])
    def get_single_currencies(code: str):
        graph = False
        request_data = dict(request.args)
        if request_data.get('graph'):
            graph = request_data.pop('graph')
        return with_graph(request_data, code=code) if graph else no_graph(request_data, code=code)
