from flask import Flask
from flask import Flask, g, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from pypipet.api.config import Config
from pypipet.api.security.identity import BLACKLIST, JTI_MAP
from pypipet.api.api_blueprint import VERSION

def create_app(project):
    app = Flask(__name__, instance_path=str(project.root), instance_relative_config=True)
    

    app.config.from_object(Config)
    
    app.config['app_context'] = project

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        username = jwt_payload['sub']['username']
        if JTI_MAP.get(username) is None:
            JTI_MAP[username] = set([jwt_payload['jti']])
        else:
            JTI_MAP[username].add(jwt_payload['jti'])
         
        return jwt_payload['jti'] in BLACKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        if JTI_MAP.get(jwt_payload['sub']['username']) is not None:
            del JTI_MAP[jwt_payload['sub']['username']]

        return jsonify({
            'message': 'token expired'
        }), 401

    if app.env == "development":
        CORS(app, origins="http://localhost:8080", supports_credentials=True)

    from .controllers.order import ordersBP
    from .controllers.valid_connection import connectionBP
    from .security.auth import authBP

    app.register_blueprint(ordersBP)
    app.register_blueprint(connectionBP)
    app.register_blueprint(authBP)
    

    @app.errorhandler(500)
    def internal_error(exception):
        # logger.info(f"Error: {exception}")
        return jsonify({"error": True, "code": str(exception)}), 500

    @app.errorhandler(404)
    def _handle(exception):
        return jsonify({"error": True, "code": str(exception)}), 404

    return app

