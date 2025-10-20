from datetime import datetime
from flask import Flask, request, jsonify, redirect
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import glob

app = Flask(__name__)

# Enhanced OpenAPI 3.0 configuration with comprehensive schema definitions
app.config['SWAGGER'] = {
    "openapi": "3.0.3",
    "info": {
        "title": "BowserAPI",
        "version": "1.0.0",
        "description": "Enhanced API with automatic contract generation\n"
                      "Демо API для демонстрации возможностей Postman.\n"
                      "Создано специально для вебинаров\n"
                      "QARATE #5: https://youtu.be/q9Xoic_14M0\n"
                      "QARATE #6: https://youtu.be/WVNVeHtmBjc",
        "contact": {
            "name": "QARATE API Support",
            "url": "https://youtu.be/q9Xoic_14M0"
        }
    },
    "servers": [
        {
            "url": "/",
            "description": "Local development server"
        }
    ],
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "1.0.0",
            "title": "BowserAPI",
            "endpoint": 'spec',
            "route": '/spec'
        }
    ],
    "components": {
        "schemas": {
            "World": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 1,
                        "description": "Unique identifier for the world"
                    },
                    "name": {
                        "type": "string",
                        "example": "World 1-1",
                        "description": "Name of the world"
                    },
                    "creationdate": {
                        "type": "string",
                        "format": "date",
                        "example": "2023-01-01",
                        "description": "Date when the world was created"
                    }
                }
            },
            "WorldInput": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "example": "World 1-1",
                        "description": "Name of the new world"
                    }
                },
                "required": ["name"]
            },
            "Castle": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 1,
                        "description": "Unique identifier for the castle"
                    },
                    "worldid": {
                        "type": "integer",
                        "example": 1,
                        "description": "ID of the world this castle belongs to"
                    },
                    "name": {
                        "type": "string",
                        "example": "Castle 1",
                        "description": "Name of the castle"
                    }
                }
            },
            "CastleInput": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "example": "Castle 1",
                        "description": "Name of the new castle"
                    }
                },
                "required": ["name"]
            },
            "Goomba": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 1,
                        "description": "Unique identifier for the Goomba"
                    },
                    "fullname": {
                        "type": "string",
                        "example": "Goomba McGoombface",
                        "description": "Full name of the Goomba"
                    },
                    "castleid": {
                        "type": "integer",
                        "example": 1,
                        "description": "ID of the castle this Goomba belongs to"
                    }
                }
            },
            "GoombaInput": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "example": "Goomba McGoombface",
                        "description": "Full name of the new Goomba"
                    },
                    "castleid": {
                        "type": "integer",
                        "example": 1,
                        "description": "ID of the castle where the Goomba will reside"
                    }
                },
                "required": ["name", "castleid"]
            },
            "WorldResponse": {
                "type": "object",
                "properties": {
                    "world": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/World"},
                        "description": "Array of world objects"
                    }
                }
            },
            "CastleResponse": {
                "type": "object",
                "properties": {
                    "castle": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/Castle"},
                        "description": "Array of castle objects"
                    }
                }
            },
            "GoombaResponse": {
                "type": "object",
                "properties": {
                    "goomba": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/Goomba"},
                        "description": "Array of goomba objects"
                    }
                }
            },
            "Error": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Not Found",
                        "description": "Error type"
                    },
                    "message": {
                        "type": "string",
                        "example": "The requested resource was not found",
                        "description": "Detailed error message"
                    }
                }
            }
        }
    }
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


with app.app_context():
    db.create_all()


def load_test_data():
    for filename in glob.glob('TestData/*.sql'):  # loading test data
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
    parameters:
      - name: worldid
        in: path
        schema:
          type: integer
        required: false
        description: ID конкретного мира (опционально)
    responses:
      200:
        description: Мир(ы) успешно возвращен(ы)
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorldResponse'
            examples:
              world_example:
                value:
                  world:
                    - id: 1
                      name: "World 1-1"
                      creationdate: "2023-01-01"
      404:
        description: Мир не найден
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    if worldid is None:
        worlds = World.query.all()
    else:
        worlds = World.query.filter_by(id=worldid).all()
    world_schema = WorldSchema(many=True)
    output = world_schema.dump(worlds)
    return jsonify({'world': output})


@app.route('/world/<int:worldid>', methods=['PUT'])
def putworld(worldid):
    """
    Обновляет выбранный мир
    ---
    tags:
      - world
    parameters:
      - name: worldid
        in: path
        schema:
          type: integer
        required: true
        description: ID мира для обновления
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/WorldInput'
    responses:
      200:
        description: Мир успешно обновлен
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorldResponse'
            examples:
              world_updated:
                value:
                  world:
                    - id: 1
                      name: "Updated World Name"
                      creationdate: "2023-01-01"
      404:
        description: Мир не найден
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    world = World.query.filter_by(id=worldid).first()
    if not world:
        return jsonify({"error": "Not Found", "message": "World not found"}), 404
    world.name = request.json['name']
    db.session.commit()
    world_schema = WorldSchema(many=False)
    output = world_schema.dump(world)
    return jsonify({'world': [output]})


@app.route('/world/<int:worldid>', methods=['DELETE'])
def deleteworld(worldid):
    """
    Удаляет выбранный мир
    ---
    tags:
      - world
    parameters:
      - name: worldid
        in: path
        schema:
          type: integer
        required: true
        description: ID мира для удаления
    responses:
      204:
        description: Мир успешно удален
      404:
        description: Мир не найден
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    world = World.query.filter_by(id=worldid).first()
    if not world:
        return jsonify({"error": "Not Found", "message": "World not found"}), 404
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
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/WorldInput'
    responses:
      201:
        description: Мир успешно добавлен
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorldResponse'
            examples:
              world_created:
                value:
                  world:
                    - id: 2
                      name: "World 1-2"
                      creationdate: "2023-01-01"
      400:
        description: Неверные данные запроса
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    if not request.json or 'name' not in request.json:
        return jsonify({"error": "Bad Request", "message": "Name is required"}), 400

    body_json = request.json
    world = World(name=body_json['name'])
    db.session.add(world)
    db.session.commit()
    world_schema = WorldSchema(many=True)
    output = world_schema.dump(World.query.filter_by(name=body_json['name']).all())
    return jsonify({'world': output}), 201


@app.route('/world/<int:worldid>/castle', methods=['GET'])
@app.route('/world/<int:worldid>/castle/<int:castleid>', methods=['GET'])
def castles(worldid, castleid=None):
    """
    Возвращает информацию о замке/замках
    ---
    tags:
      - castle
    parameters:
      - name: worldid
        in: path
        schema:
          type: integer
        required: true
        description: ID мира
      - name: castleid
        in: path
        schema:
          type: integer
        required: false
        description: ID конкретного замка (опционально)
    responses:
      200:
        description: Замок(и) успешно возвращен(ы)
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CastleResponse'
            examples:
              castle_example:
                value:
                  castle:
                    - id: 1
                      worldid: 1
                      name: "Castle 1"
      404:
        description: Замок не найден
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    if castleid is None:
        castles = Castle.query.filter_by(worldid=worldid).all()
    else:
        castles = Castle.query.filter_by(worldid=worldid, id=castleid).all()
    castle_schema = CastleSchema(many=True)
    output = castle_schema.dump(castles)
    return jsonify({'castle': output})


@app.route('/world/<int:worldid>/castle', methods=['POST'])
def addcastle(worldid):
    """
    Добавляет новый замок
    ---
    tags:
      - castle
    parameters:
      - name: worldid
        in: path
        schema:
          type: integer
        required: true
        description: ID мира, в который добавляется замок
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CastleInput'
    responses:
      201:
        description: Замок успешно добавлен
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CastleResponse'
            examples:
              castle_created:
                value:
                  castle:
                    - id: 2
                      worldid: 1
                      name: "Castle 2"
      400:
        description: Неверные данные запроса
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    if not request.json or 'name' not in request.json:
        return jsonify({"error": "Bad Request", "message": "Name is required"}), 400

    body_json = request.json
    castle = Castle(worldid=worldid, name=body_json['name'])
    db.session.add(castle)
    db.session.commit()
    castle_schema = CastleSchema(many=True)
    output = castle_schema.dump(Castle.query.filter_by(name=body_json['name']).all())
    return jsonify({'castle': output}), 201


@app.route('/world/<int:worldid>/castle/<int:castleid>', methods=['DELETE'])
def deletecastle(worldid, castleid):
    """
    Удаляет выбранный замок
    ---
    tags:
      - castle
    parameters:
      - name: worldid
        in: path
        schema:
          type: integer
        required: true
        description: ID мира
      - name: castleid
        in: path
        schema:
          type: integer
        required: true
        description: ID замка для удаления
    responses:
      204:
        description: Замок успешно удален
      404:
        description: Замок не найден
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    castle = Castle.query.filter_by(worldid=worldid, id=castleid).first()
    if not castle:
        return jsonify({"error": "Not Found", "message": "Castle not found"}), 404
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
    parameters:
      - name: worldid
        in: path
        schema:
          type: integer
        required: true
        description: ID мира
      - name: goombaid
        in: path
        schema:
          type: integer
        required: false
        description: ID конкретной гумбы (опционально)
    responses:
      200:
        description: Гумба(ы) успешно возвращен(ы)
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GoombaResponse'
            examples:
              goomba_example:
                value:
                  goomba:
                    - id: 1
                      fullname: "Goomba McGoombface"
                      castleid: 1
      404:
        description: Гумба не найден
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    if goombaid is None:
        goombas = Goomba.query.filter_by(worldid=worldid).all()
    else:
        goombas = Goomba.query.filter_by(worldid=worldid, id=goombaid).all()
    goomba_schema = GoombaSchema(many=True)
    output = goomba_schema.dump(goombas)
    return jsonify({'goomba': output})


@app.route('/world/<int:worldid>/goomba', methods=['POST'])
def addgoomba(worldid):
    """
    Добавляет нового гумбу
    ---
    tags:
      - goomba
    parameters:
      - name: worldid
        in: path
        schema:
          type: integer
        required: true
        description: ID мира, в который добавляется гумба
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/GoombaInput'
    responses:
      201:
        description: Гумба успешно добавлен
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GoombaResponse'
            examples:
              goomba_created:
                value:
                  goomba:
                    - id: 2
                      fullname: "Goomba Junior"
                      castleid: 1
      400:
        description: Неверные данные запроса
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    if not request.json or 'name' not in request.json or 'castleid' not in request.json:
        return jsonify({"error": "Bad Request", "message": "Name and castleid are required"}), 400

    body_json = request.json
    goomba = Goomba(worldid=worldid, castleid=body_json['castleid'], fullname=body_json['name'])
    db.session.add(goomba)
    db.session.commit()
    goomba_schema = GoombaSchema(many=True)
    output = goomba_schema.dump(Goomba.query.filter_by(fullname=body_json['name']).all())
    return jsonify({'goomba': output}), 201


@app.route('/world/<int:worldid>/goomba/<int:goombaid>', methods=['DELETE'])
def deletegoomba(worldid, goombaid):
    """
    Удаляет выбранного гумбу
    ---
    tags:
      - goomba
    parameters:
      - name: worldid
        in: path
        schema:
          type: integer
        required: true
        description: ID мира
      - name: goombaid
        in: path
        schema:
          type: integer
        required: true
        description: ID гумбы для удаления
    responses:
      204:
        description: Гумба успешно удален
      404:
        description: Гумба не найден
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    goomba = Goomba.query.filter_by(worldid=worldid, id=goombaid).first()
    if not goomba:
        return jsonify({"error": "Not Found", "message": "Goomba not found"}), 404
    db.session.delete(goomba)
    db.session.commit()
    return ('', 204)


@app.route('/tos')
def tos():
    """
    Terms of Service
    ---
    tags:
      - misc
    responses:
      200:
        description: Terms of Service page
        content:
          text/html:
            schema:
              type: string
    """
    response = """
    <iframe src="https://giphy.com/embed/l0K4n42JVSqqUvAQg" width="480" height="297" frameBorder="0"
    class="giphy-embed" allowFullScreen></iframe><p>
    <a href="https://giphy.com/gifs/chuber-qa-quality-assurance-l0K4n42JVSqqUvAQg">via GIPHY</a></p>"""
    return response


if __name__ == '__main__':
    app.run(debug=True)
