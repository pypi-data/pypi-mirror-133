from pypipet.core.shop_conn.shop_connector import ShopConnector
from pypipet.core.operations.utility import get_front_shop_id


def setup_front_shop(ctx, session, shop_name):
    shop_conn = ctx.get_shop_connector(shop_name)
    get_front_shop_id(ctx.get_table_objects(), session, shop_conn)

def get_session(ctx):
    sessionmaker = ctx.get_session_maker()
    session = sessionmaker()
    return session