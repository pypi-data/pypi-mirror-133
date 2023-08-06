from django import template
from db_hj3415 import setting, mongo
from krx_hj3415 import krx

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

register = template.Library()


@register.inclusion_tag('dbmanager/setting.html', takes_context=True)
def dbsetting(context):
    status = setting.load()
    if status.mongo_addr.startswith('mongodb://') and status.mongo_addr.endswith(':27017'):
        context['mongo'] = {'addr': status.mongo_addr[10:-6], 'activate': status.active_mongo}
    else:
        # if address is invalid, set localhost address
        context['mongo'] = {'addr': '127.0.0.1', 'activate': status.active_mongo}

    context.update({'sqlite': {'addr': status.sqlite3_path, 'activate': status.active_sqlite3},
                    'all_corps_dbs': mongo.Corps.get_all_corps() if status.active_mongo else None,
                    'all_mi_cols': mongo.MI().get_all_col() if status.active_mongo else None,
                    'len_krx': len(krx.get_codes())})
    logger.debug(f'setting_context : {context}')
    return context