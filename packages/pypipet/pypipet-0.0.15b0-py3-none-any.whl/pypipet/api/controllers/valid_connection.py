from flask import jsonify, request, current_app, Blueprint
from .utility import setup_front_shop,get_session
# import db connection

connectionBP = Blueprint('connection', __name__, url_prefix='/echo')

@connectionBP.route('/', methods=['GET'])
def test():
    ctx = current_app.config['app_context']
    session = get_session(ctx)
    valid = session is not None
    session.close()
    
    return jsonify({'connection': valid})

