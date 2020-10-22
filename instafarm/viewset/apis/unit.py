import hashlib

from flask import request, session, render_template
from instafarm import app
from datetime import datetime
from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict, send_mail

@app.route('/apis/unit/add', methods = ['POST']) 
def unit_add():
    print('unit/add')
    data = {}
    try:
        data = get_request_dict()
        if not ('token' in data) or data['token'] == '' or \
            not ('name' in data) or data['name'] == '':
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
        if model.Unit.find_by_name(data['name']):
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.exist_error,
                'message': model.ResponseText.exist_error,
            })
        unit = model.Unit(data['name'])
        model.add(unit)
        model.commit()
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : unit.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/unit/getall', methods = ['POST']) 
def unit_getall():
    print('unit/getall')
    data = {}
    try:
        data = get_request_dict()
        if not ('token' in data) or data['token'] == '':
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
        results = [unit.to_dict() for unit in model.Unit.get_all()]
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


@app.route('/apis/unit/getbyid', methods = ['POST']) 
def unit_getbyid():
    print('unit/getbyid')
    data = {}
    try:
        data = get_request_dict()
        if not ('token' in data) or data['token'] == '' or \
            not ('unitid' in data) or data['unitid'] == '':
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
        
        unit = model.Unit.get_by_id(data['unitid'])
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : unit.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/unit/update', methods = ['POST']) 
def unit_update():
    print('unit/update')
    data = {}
    try:
        data = get_request_dict()
        if not ('token' in data) or data['token'] == '' or \
            not ('unitid' in data) or data['unitid'] == '' or \
            not ('name' in data) or data['name'] == '':
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
        unit = model.Unit.get_by_id(data['unitid'])
        if not unit:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        if model.Unit.find_by_name(data['name']):
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.exist_error,
                'message': model.ResponseText.exist_error,
            })
        unit.name = data['name']
        model.add(unit)
        model.commit()
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : unit.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/unit/delete', methods = ['POST'])
def unit_delete():
    print('unit/delete')
    data = {}
    try:
        data = get_request_dict()
        if not ('token' in data) or data['token'] == '' or \
            not ('unitid' in data) or data['unitid'] == '':
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
        unit = model.Unit.get_by_id(data['unitid'])
        if not unit:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        model.delete(unit)
        model.commit()
        results = [unit.to_dict() for unit in model.Unit.get_all()]
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

