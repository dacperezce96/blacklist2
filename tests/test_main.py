from unittest import TestCase
from faker import Faker, providers
import json

from modelos.modelos import BlackUser, db
from application import application

class TestUtilidades(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = application.test_client()
        application.app_context().push()
        self.email = self.data_factory.email()
        self.user = BlackUser(
            email = self.email,
            app_uuid = self.data_factory.uuid4(),
            blocked_reason = self.data_factory.word(),
            ip = self.data_factory.ipv4()
        )
        db.session.add(self.user)        
        db.session.commit()

    def tearDown(self) -> None:        
        db.session.delete(self.user)
        db.session.commit()

    def test_crear_black_user(self):
        nuevo_usuario ={            
            "email": self.data_factory.email(),
            "app_uuid": self.data_factory.uuid4(),
            "blocked_reason": self.data_factory.text()
        }
        solicitud_nuevo_usuario = self.client.post(
            "/blacklists",
            data = json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer token'}
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 201)
        id = solicitud_nuevo_usuario.json['entidad']['id']
        usuario = BlackUser.query.get(id)                
        db.session.delete(usuario)
        db.session.commit()
    

    def test_consultar_black_user(self):
        solicitud_nuevo_usuario = self.client.get(
            f"/blacklists/{self.email}",
            headers={'Authorization': 'Bearer token'}
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 200)
    

    def test_ping(self):
        solicitud_nuevo_usuario = self.client.get(
            f"/ping",
            headers={'Authorization': 'Bearer token'}
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 200)