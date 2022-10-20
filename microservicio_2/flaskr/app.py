from flaskr import create_app
from flask_restful import Api, Resource
from .modelos import db, Cancion, CancionSchema

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cancion_schema = CancionSchema()

class VistaTablaPuntaje(Resource):

    def get(self):
        return[cancion_schema.dump(cancion) for cancion in Cancion.query.all()]

api = Api(app)
api.add_resource(VistaTablaPuntaje, '/tablaPuntajes')