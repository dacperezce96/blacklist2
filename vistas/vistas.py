from flask_restful import Resource
from modelos.modelos import db, BlackUser, BlackUserSchema
from flask import request, Response
import os

black_user_schema = BlackUserSchema()

class VistaBlackList(Resource):
    def post(self):
        respuesta_token = validar_token()
        if not respuesta_token:
            return Response(status=401)
        else:
            if not request.is_json:
                return Response(status=400)
            parse_json = request.get_json()
            if parse_json.get('email', None) and parse_json.get('app_uuid', None) and parse_json.get('blocked_reason', None):
                nuevo_usuario = BlackUser(
                    email = parse_json.get('email', None),
                    app_uuid = parse_json.get('app_uuid', None),
                    blocked_reason = parse_json.get('blocked_reason', None),
                    ip = request.remote_addr
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                return {
                    "message": "Añadido correctamente a la lista negra",
                    "entidad": black_user_schema.dump(nuevo_usuario)
                }, 201
            else:
                return Response(status=400)
            
class VistaBlackUser(Resource):
    def get(self, email):
        respuesta_token = validar_token()
        if not respuesta_token:
            return Response(status=401)
        else:
            usuario = BlackUser.query.filter_by(email=email).all()
            if len(usuario) > 0:
                return {
                    "message": True,
                    "blocked_reason": usuario[0].blocked_reason,
                    "entidad": black_user_schema.dump(usuario[0])
                }, 200
            else:
                return{
                    "message":False
                }, 200


def validar_token():
    token_ok = os.getenv('TOKEN', "token")
    headers = request.headers.get('Authorization')
    token_request = headers.split(" ")[-1]
    if token_ok == token_request:
        return True
    else:
        return False