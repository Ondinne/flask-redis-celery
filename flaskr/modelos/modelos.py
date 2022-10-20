from flask_sqlalchemy import SQLAlchemy
import enum
#Se importa para serialización y deserialización
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

#Para la relación entre Album y Canción (es una relación muchos a muchos compuesta -> Un álbum
# puede tener muchas canciones y una canción puede pertenecer a muchos álbumes, entonces se crea
# esta tabla)
albumes_canciones = db.Table('album_cancion',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True),
    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'),primary_key=True))

class Cancion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    minutos = db.Column(db.Integer)
    segundos = db.Column(db.Integer)
    interprete = db.Column(db.String(128))
    #Relación muchos a muchos
    albumes = db.relationship('Album', secondary='album_cancion', back_populates="canciones")

#PRUEBA
    # def __repr__(self):
    #     return "{}-{}-{}-{}".format(self.titulo, self.minutos, self.segundos, self.interprete)

class Medio(enum.Enum):
    DISCO = 1
    CASETE = 2
    CD = 3

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(128))
    anio = db.Column(db.Integer)
    descripcion = db.Column(db.String(256))
    medio = db.Column(db.Enum(Medio))
    #Implementación de las relaciones (un álbum puede pertenecer solo a un único usuario)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    #Relación muchos a muchos con canciones
    canciones = db.relationship('Cancion', secondary='album_cancion',back_populates="albumes")
    #Para evitar que los títulos de los álbumes se dupliquen
    #Se le agrega la coma al final para indicarle a python que vendrá en forma de tupla
    __table_args__ = (db.UniqueConstraint('usuario', 'titulo', name='titulo_unico_album'),)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60))
    contrasenia = db.Column(db.String(20))
    #Implementación de las relaciones (en este caso 1 usuario puede tener muchos albumes)
    albumes = db.relationship('Album', cascade='all, delete, delete-orphan')

#Para serializar las enumeraciones
class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'llave':value.name, 'valor':value.value}

#Para serializar el álbum
class AlbumSchema(SQLAlchemyAutoSchema):
    medio = EnumADiccionario(attribute=('medio'))
    class Meta:
        model = Album
        include_relationships = True
        load_instance = True

class CancionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cancion
        include_relationships = True
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True