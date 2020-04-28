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
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "0.0.1",
            "title": "BowserApi",
            "endpoint": 'spec',
            "description": 'Демо API для демонстрации возможностей Postman.\n'
                           'Создано специально для вебинара QARATE #5: https://youtu.be/q9Xoic_14M0',
            "route": '/spec'
        }
    ]
}

swagger = Swagger(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
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

for filename in glob.glob('TestData/*.sql'): # loading test data
    with open(filename, 'r') as test_data_file:
        query = test_data_file.read()
        db.engine.execute(query)
        db.session.commit()

class WorldSchema(ma.ModelSchema):
    class Meta:
        model = World

class CastleSchema(ma.ModelSchema):
    class Meta:
        model = Castle

class GoombaSchema(ma.ModelSchema):
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
        Удалет выбранный мир
        ---
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

@app.route('/world/<int:worldid>/goomba', methods=['GET'])
@app.route('/world/<int:worldid>/goomba/<int:goombaid>', methods=['GET'])
def goombas(worldid, goombaid=None):
    """
        Возвращает информацию о гумбе/гумбах
        ---
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

@app.route('/tos')
def tos():
    response = """
    <iframe src="https://giphy.com/embed/l0K4n42JVSqqUvAQg" width="480" height="297" frameBorder="0"
    class="giphy-embed" allowFullScreen></iframe><p>
    <a href="https://giphy.com/gifs/chuber-qa-quality-assurance-l0K4n42JVSqqUvAQg">via GIPHY</a></p>"""
    return response