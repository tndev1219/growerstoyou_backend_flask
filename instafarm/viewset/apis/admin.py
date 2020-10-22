import hashlib

from flask import request, session, render_template
from instafarm import app
from datetime import datetime
from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict, send_mail


@app.route('/apis/admin/getuserbyid', methods = ['POST']) 
def admin_getuserbyid():
    print('admin/getuserbyid')
    data = {}
    keys  = ['token', 'userid']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['token'] is None or data['token'] == '' or \
            data['userid'] is None or data['userid'] == '':
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
        person = model.User.find_by_id(data['userid'])
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : person.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })


@app.route('/apis/admin/getuserbyrole', methods = ['POST']) 
def admin_getuserbyrole():
    print('admin/getuserbyrole')
    data = {}
    keys  = ['token', 'role']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['token'] is None or data['token'] == '' or \
            data['role'] is None or data['role'] == '':
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
        results = [person.to_dict() for person in model.User.get_by_role(data['role'])] 
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : results
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })


@app.route('/apis/admin/getuserbyrolestatus', methods = ['POST']) 
def admin_getuserbyrolestatus():
    print('admin/getuserbyrolestatus')
    data = {}
    keys  = ['token', 'role', 'status']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['token'] is None or data['token'] == '' or \
            data['status'] is None or data['status'] == '' or \
            data['role'] is None or data['role'] == '':
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
        results = [person.to_dict() for person in model.User.get_by_role_status(data['role'], data['status'])] 
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : results
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/admin/setstatus', methods = ['POST']) 
def admin_setstatus():
    print('admin/setstatus')
    data = {}
    keys  = ['token', 'userid', 'status']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['token'] is None or data['token'] == '' or \
            data['userid'] is None or data['userid'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        # admin = model.User.find_by_token(data['token'])
        # if not admin or admin.role != 0:
        #     return json_response({
        #         'success': False,
        #         'errcode': model.ResponseCode.no_exist,
        #         'message': model.ResponseText.no_exist,
        #     })
        user = model.User.find_by_id(data['userid'])
        if not user:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        user.status = data['status']
        model.add(user)
        model.commit()
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : user.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })
