from flask import jsonify, request

from app.domain.service import CurrencyService


def create_routing(app):
    @app.route('/currency', methods=['GET'])
    def get_all_currencies():
        return jsonify({'result': CurrencyService().pull_many_currencies_from_api(**request.args).get_currency()})

    @app.route('/currency/<string:code>', methods=['GET'])
    def get_single_currencies(code: str):
        return jsonify({'result': CurrencyService().pull_currency_from_api(code, **request.args).get_currency()})

    # TODO dodac mozliwosc wysylania wykresu

