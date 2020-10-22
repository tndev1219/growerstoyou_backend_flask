import os
import hashlib

from flask import request, send_from_directory
from instafarm import app
from datetime import datetime
from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict, allow_extention


@app.route('/apis/basket/add', methods = ['POST'])
def basket_add():
    print('basket/add')
    data = {}
    keys = ['token', 'productid', 'count']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['token'] is None or data['token'] == '' or \
            data['productid'] is None or data['productid'] == '' or \
            data['count'] is None or data['count'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        user = model.Basket.user_by_token(data['token'])
        if not user:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        product = model.Basket.get_by_id_status(data['productid'], 0)
        if product:
            product.count += int(data['count'])
            model.add(product)
            model.commit()
            return json_response({
                'success': True,
                'message': model.ResponseText.success,
            })
    
        basket = model.Basket()
        basket.userid = user.id
        basket.productid = data['productid']
        basket.count = data['count']
        basket.status = 0
        model.add(basket)
        model.commit()
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/basket/update', methods = ['POST'])
def basket_update():
    print('basket/update')
    data = {}
    keys = ['token', 'id', 'count']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['token'] is None or data['token'] == '' or \
            data['id'] is None or data['id'] == '' or \
            data['count'] is None or data['count'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })

        basket = model.Basket.get_by_id(data['id'])
        
        if not basket:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        if (int(data['count']) > int(basket.productinfo.count)):
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.beyond,
                'message': model.ResponseText.beyond,
            })
        basket.count = data['count']
        model.add(basket)
        model.commit()
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'result': basket.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })


@app.route('/apis/basket/getall', methods = ['POST'])
def basket_getall():
    print('basket/getall')
    try:
        data = {}
        keys = ['token']
        for key in keys:
            data[key] = get_request(key, None)
        if data['token'] is None or data['token'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        results = [basket.to_dict() for basket in model.Basket.get_by_status(0)]
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': results
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })


@app.route('/apis/basket/getbyuserid', methods = ['POST'])
def basket_getbyuserid():
    print('basket/getbyuserid')
    data = {}
    keys = ['token', 'userid']
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
        # user = model.Basket.user_by_token(data['token'])
        # if not user:
        #     return json_response({
        #         'success': False,
        #         'errcode': model.ResponseCode.no_exist,
        #         'message': model.ResponseText.no_exist,
        #     })
        cart = model.Basket.get_by_userid(data['userid'])
        # cart = model.Basket.get_by_status(0)
        results = [order.to_dict() for order in cart]
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': results
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/basket/delete', methods = ['POST']) # not in active
def basket_delete():
    print('basket/delete')
    data = {}
    keys = ['token','id']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['id'] is None or data['id'] == '' or \
            data['token'] is None or data['token'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        basket = model.Basket.get_by_id(int(data['id']))
        model.delete(basket)
        model.commit()
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/basket/getbyids', methods = ['POST']) # not in active
def basket_getbyids():
    print('basket/getbyids')
    data = {}
    keys = ['token','ids']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['ids'] is None or data['ids'] == '' or \
            data['token'] is None or data['token'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        basket = model.Basket.get_by_ids(data['ids'])
        results = [item.to_dict() for item in basket]
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': results
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })