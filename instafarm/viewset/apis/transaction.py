import hashlib
import stripe

from flask import request, session, render_template
from instafarm import app
from datetime import datetime

from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict, send_mail

stripe.api_key = app.config['STRIP_SECRET_KEY']

@app.route('/apis/transaction/getall', methods = ['POST'])
def transaction_getall():
    print('transaction/getall')
    data = {}
    keys = ['token', 'offset', 'limit', 'keyword']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['token'] is None or data['token'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        user = model.User.find_by_token(data['token'])
        if not user:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        offset = 0
        limit  = 50000
        keyword = ''
        if ('offset' in data) and data['offset'] != '':
            offset = data['offset']
        if ('limit' in data) and data['limit'] != '':
            limit = data['limit']
        if ('keyword' in data) and data['keyword'] != '':
            keyword = data['keyword']
        transactions = model.Transaction.get_all(offset, limit, keyword)
        results = []
        no = 1
        for transaction in transactions['data']:
            result = transaction.to_dict()
            result['no'] = no
            results.append(result)
            no += 1
        allcount = transactions['count']
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': results,
            'allcount': allcount
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

    
@app.route('/apis/transaction/getbyuserid', methods = ['POST'])
def transaction_getbyuserid():
    print('transaction/getbyuserid')
    data = {}
    keys = ['token', 'userid', 'offset', 'limit', 'keyword']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['userid'] is None or data['userid'] == '' or \
            data['token'] is None or data['token'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        user = model.User.find_by_token(data['token'])
        if not user:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        offset = 0
        limit  = 50000
        keyword = ''
        if ('offset' in data) and data['offset'] != '':
            offset = data['offset']
        if ('limit' in data) and data['limit'] != '':
            limit = data['limit']
        if ('keyword' in data) and data['keyword'] != '':
            keyword = data['keyword']
        transactions = model.Transaction.get_by_userid(data['userid'], offset, limit, keyword)['data']
        results = []
        no = 1
        for transaction in transactions:
            result = transaction.to_dict()
            result['no'] = no
            results.append(result)
            no += 1
        allcount = model.Transaction.get_by_userid(data['userid'], offset, limit, keyword)['count']
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': results,
            'allcount': allcount
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })