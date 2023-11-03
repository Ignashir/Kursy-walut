from flask_restful import Api

from app.infrastructure.web.configuration import app
from app.infrastructure.web.routes import route
from app.infrastructure.web.routes.resources.gold_resource import GoldResource


def web_app():
    with app.app_context():
        api = Api(app)
        route.create_routing(app)
        api.add_resource(GoldResource, '/gold')
        return app
