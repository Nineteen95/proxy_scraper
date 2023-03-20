from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Proxy
from proxy_checker import check_proxy
from datetime import datetime, timedelta
import os

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')


app = Flask(__name__)
api = Api(app)
CORS(app)

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}')
Session = sessionmaker(bind=engine)
session = Session()
'''Данный код создает Flask-приложение и RESTful API, позволяющий получать список доступных прокси из базы данных и проверять их статус. Мы также добавляем CORS-поддержку для обработки запросов из других источников.

    Для работы с базой данных мы используем SQLAlchemy и моделируем таблицу Proxy. Мы также импортируем модуль proxy_checker для
    '''

def serialize_proxy(proxy):
    return {
        'id': proxy.id,
        'ip_address': proxy.ip_address,
        'port': proxy.port,
        'status': proxy.status,
        'last_checked': str(proxy.last_checked),
        'country': proxy.country
    }
def start_api_server(host, port):
    app.run(host=host, port=port, debug=True)

class ProxyList(Resource):
    def get(self):
        proxies = session.query(Proxy).filter(Proxy.status == 'OK').all()
        serialized_proxies = [serialize_proxy(proxy) for proxy in proxies]
        return jsonify({'proxies': serialized_proxies})


class ProxyChecker(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip_address', required=True)
        parser.add_argument('port', type=int, required=True)
        args = parser.parse_args()
        ip_address = args['ip_address']
        port = args['port']

        try:
            proxy_status = check_proxy(ip_address, port)
        except Exception as e:
            abort(500, message='Error while checking proxy: {}'.format(str(e)))

        try:
            proxy = session.query(Proxy).filter_by(ip_address=ip_address, port=port).first()
            if proxy:
                proxy.status = proxy_status
                proxy.last_checked = datetime.utcnow()
            else:
                new_proxy = Proxy(ip_address=ip_address, port=port, status=proxy_status, last_checked=datetime.utcnow())
                session.add(new_proxy)
            session.commit()
            return jsonify({'ip_address': ip_address, 'port': port, 'status': proxy_status})
        except SQLAlchemyError as e:
            session.rollback()
            abort(500, message='Error while saving proxy status: {}'.format(str(e)))


api.add_resource(ProxyList, '/proxies')
api.add_resource(ProxyChecker, '/check')

if __name__ == '__main__':
    app.run(debug=True)
