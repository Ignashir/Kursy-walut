from flask_restful import Api
from flask_cors import CORS
from app.infrastructure.web.configuration import app
from app.infrastructure.web.routes import route
from app.infrastructure.web.routes.resources.gold_resource import GoldResource, GoldPredictor


def web_app():
    with app.app_context():
        cors_config = {
            'allow_headers': ['accept, accept-encoding', 'content-type', 'authorization'],
            'methods': ['get'],
            'origins': ['http://localhost:3000']
        }
        CORS(app, resources={'/*': cors_config})
        api = Api(app)
        route.create_routing(app)
        api.add_resource(GoldPredictor, '/gold/predict/<string:date_to_predict>')
        api.add_resource(GoldResource, '/gold')
        return app
