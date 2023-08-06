from flask import jsonify, request, current_app
from pypipet.api.api_blueprint import APIBlueprint
from pypipet.api.security.auth import validate_access
from .utility import setup_front_shop,get_session
from pypipet.core.operations.order import get_order_info, get_orders
from flask_jwt_extended import jwt_required,get_jwt_identity

ordersBP = APIBlueprint('orders', __name__)


@ordersBP.route('/order/<order_id>', methods=['GET'])
@jwt_required()
@validate_access(1)
def get_order(order_id):
    ctx = current_app.config['app_context']
    session = get_session(ctx)
    order = get_order_info(ctx.get_table_objects(), 
          session, {'id': int(order_id)}, item_info=True)
    
    session.close()
    return jsonify(order)

@ordersBP.route('/orders', methods=['POST'])
@jwt_required()
@validate_access(1)
def get_order_list():
    data =  request.get_json()
    ctx = current_app.config['app_context']
    session = get_session(ctx)
    orders = get_orders(ctx.get_table_objects(),session, data)
    session.close()
    return jsonify(orders)

@ordersBP.route('/test', methods=['POST'])
@jwt_required()
def test():
    return jsonify({'message': 'test'})