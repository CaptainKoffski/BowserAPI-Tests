from datetime import datetime
from flask import Flask, json, request, jsonify, Response, redirect
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import glob


app = Flask(__name__)

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Flasgger",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "0.0.1",
            "title": "BowserApi",
            "endpoint": 'spec',
            "description": 'Демо API для демонстрации возможностей Postman.\n'
                           'Создано специально для вебинаров\n'
                           'QARATE #5: https://youtu.be/q9Xoic_14M0\n'
                           'QARATE #6: https://youtu.be/WVNVeHtmBjc',
            "route": '/spec'
        }
    ]
}

swagger = Swagger(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bowser.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    db.UniqueConstraint(name)
    creationdate = db.Column(db.Date, default=datetime.now)

class Castle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worldid = db.Column(db.Integer, db.ForeignKey('world.id'))
    name = db.Column(db.String)

class Goomba(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String)
    worldid = db.Column(db.Integer, db.ForeignKey('world.id'))
    castleid = db.Column(db.Integer, db.ForeignKey('castle.id'))

db.create_all()

def load_test_data():
    for filename in glob.glob('TestData/*.sql'): # loading test data
        with open(filename, 'r') as test_data_file:
            query = test_data_file.read()
            db.engine.execute(query)
            db.session.commit()

class WorldSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = World

class CastleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Castle

class GoombaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Goomba
        fields = ('id', 'fullname', 'castleid')

@app.route('/')
def root():
    return redirect("/apidocs/", code=302)

@app.route('/world', methods=['GET'])
@app.route('/world/<int:worldid>', methods=['GET'])
def getworld(worldid=None):
    """
        Возвращает информацию о мире/мирах
        ---
        tags:
            - world
        responses:
          200:
            description: Мир возвращен
    """
    if worldid is None:
        worlds = World.query.all()
    else:
        worlds = World.query.filter_by(id=worldid).all()
    world_schema = WorldSchema(many=True)
    output = world_schema.dump(worlds)
    return jsonify({ 'world': output })

@app.route('/world/<int:worldid>', methods=['PUT'])
def putworld(worldid):
    """
        Обновляет выбранный мир
        ---
        tags:
            - world
        responses:
          200:
            description: Мир успешно обновлен
    """
    world = World.query.filter_by(id=worldid).first()
    world.name = request.json['name']
    db.session.commit()
    world_schema = WorldSchema(many=False)
    output = world_schema.dump(world)
    return jsonify({ 'world': output })

@app.route('/world/<int:worldid>', methods=['DELETE'])
def deleteworld(worldid):
    """
        Удаляет выбранный мир
        ---
        tags:
            - world
        responses:
          204:
            description: Мир удален
    """
    world = World.query.filter_by(id=worldid).first()
    db.session.delete(world)
    db.session.commit()
    return ('', 204)

@app.route('/addworld', methods=['POST'])
def addworld():
    """
        Добавляет новый мир
        ---
        tags:
            - world
        responses:
          200:
            description: Мир добавлен
    """
    body_json = request.json
    world = World(name=body_json['name'])
    db.session.add(world)
    db.session.commit()
    world_schema = WorldSchema(many=True)
    output = world_schema.dump(World.query.filter_by(name=body_json['name']).all())
    return jsonify({ 'world' : output })

@app.route('/world/<int:worldid>/castle', methods=['GET'])
@app.route('/world/<int:worldid>/castle/<int:castleid>', methods=['GET'])
def castles(worldid, castleid=None):
    """
        Возвращает информацию о замке/замках
        ---
        tags:
            - castle
        responses:
          200:
            description: Замок/замки возвращен/возвращены
    """
    if castleid is None:
        castles = Castle.query.filter_by(worldid=worldid).all()
    else:
        castles = Castle.query.filter_by(worldid=worldid, id=castleid).all()
    castle_schema = CastleSchema(many=True)
    output = castle_schema.dump(castles)
    return jsonify({ 'castle': output })

@app.route('/world/<int:worldid>/castle', methods=['POST'])
def addcastle(worldid):
    """
        Добавляет новый замок
        ---
        tags:
            - castle
        responses:
          200:
            description: Замок добавлен
    """
    body_json = request.json
    castle = Castle(worldid=worldid, name=body_json['name'])
    db.session.add(castle)
    db.session.commit()
    castle_schema = CastleSchema(many=True)
    output = castle_schema.dump(Castle.query.filter_by(name=body_json['name']).all())
    return jsonify({'castle': output})

@app.route('/world/<int:worldid>/castle/<int:castleid>', methods=['DELETE'])
def deletecastle(worldid, castleid):
    """
        Удаляет выбранный замок
        ---
        tags:
            - castle
        responses:
          204:
            description: Замок удален
    """
    castle = Castle.query.filter_by(worldid=worldid, id=castleid).first()
    db.session.delete(castle)
    db.session.commit()
    return ('', 204)

@app.route('/world/<int:worldid>/goomba', methods=['GET'])
@app.route('/world/<int:worldid>/goomba/<int:goombaid>', methods=['GET'])
def goombas(worldid, goombaid=None):
    """
        Возвращает информацию о гумбе/гумбах
        ---
        tags:
            - goomba
        responses:
          200:
            description: Гумба/гумбы возвращен/возвращены
    """
    if goombaid is None:
        goombas = Goomba.query.filter_by(worldid=worldid).all()
    else:
        goombas = Goomba.query.filter_by(worldid=worldid, id=goombaid).all()
    goomba_schema = GoombaSchema(many=True)
    output = goomba_schema.dump(goombas)
    return jsonify({ 'goomba': output })

@app.route('/world/<int:worldid>/goomba', methods=['POST'])
def addgoomba(worldid):
    """
        Добавляет нового гумбу
        ---
        tags:
            - goomba
        responses:
          200:
            description: Гумба добавлен
    """
    body_json = request.json
    goomba = Goomba(worldid=worldid, castleid=body_json['castleid'], name=body_json['name'])
    db.session.add(goomba)
    db.session.commit()
    goomba_schema = GoombaSchema(many=True)
    output = goomba_schema.dump(Goomba.query.filter_by(name=body_json['name']).all())
    return jsonify({'goomba': output})

@app.route('/world/<int:worldid>/goomba/<int:goombaid>', methods=['DELETE'])
def deletegoomba(worldid, goombaid):
    """
        Удаляет выбранного гумбу
        ---
        tags:
            - goomba
        responses:
          204:
            description: Гумба удален
    """
    goomba = Goomba.query.filter_by(worldid=worldid, id=goombaid).first()
    db.session.delete(goomba)
    db.session.commit()
    return ('', 204)

@app.route('/tos')
def tos():
    response = """
    <iframe src="https://giphy.com/embed/l0K4n42JVSqqUvAQg" width="480" height="297" frameBorder="0"
    class="giphy-embed" allowFullScreen></iframe><p>
    <a href="https://giphy.com/gifs/chuber-qa-quality-assurance-l0K4n42JVSqqUvAQg">via GIPHY</a></p>"""
    return response