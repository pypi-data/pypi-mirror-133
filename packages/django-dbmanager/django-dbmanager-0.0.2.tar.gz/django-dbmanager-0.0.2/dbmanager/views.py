from django.shortcuts import render, HttpResponseRedirect
from db_hj3415 import setting as dbsetting
from django.contrib import messages

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def test(request):
    # dbsetting.chg_mongo_addr('mongodb://192.168.0.173:27017')
    return render(request, "dbmanager/test.html", {})


def setting(request):
    status = dbsetting.load()
    m = ''
    if request.method == 'POST':
        logger.info(f'post : {request.POST}')
        dbsetting.turn_on_mongo() if 'mongo_activate' in request.POST else None
        dbsetting.chg_mongo_addr('mongodb://' + request.POST.get('mongo_new_addr', status.mongo_addr) + ':27017')
        dbsetting.turn_on_sqlite3() if 'sqlite_activate' in request.POST else dbsetting.turn_off_sqlite3()
        dbsetting.chg_sqlite3_path(request.POST.get('sqlite_new_addr', status.sqlite3_path))
        m = f"Database set."

    messages.add_message(request, messages.SUCCESS, m)
    logger.debug(f'message : {m}')

    # How to redirect previous page
    # https://stackoverflow.com/questions/35796195/how-to-redirect-to-previous-page-in-django-after-post-request/35796330
    prev_path = request.POST.get('next', '/')
    logger.debug(f'prev : {prev_path}')
    return HttpResponseRedirect('/' if prev_path == '' else prev_path)
