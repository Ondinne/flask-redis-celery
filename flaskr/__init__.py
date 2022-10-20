from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial_canciones.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #se añade para el JWT
    #la secret key permite validar los tokens que se reciban
    app.config['JWT_SECRET_KEY']='frase-secreta'
    #se añade configuración para permitir propagación de excepciones
    #Esta opción indica a los errores de una forma más clara que un internal server error
    app.config['PROPAGATE_EXCEPTIONS']=True

    return app