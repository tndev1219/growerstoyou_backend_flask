import hashlib

from flask import request, session, render_template
from instafarm import app
from datetime import datetime
from base64 import b64encode, b64decode
from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict, send_mail


@app.route('/apis/profile/getuser', methods = ['POST']) 
def profile_getbyuserid():
    print('profile/getuser')
    data = {}
    keys  = ['token']
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

@app.route('/apis/profile/update', methods = ['POST'])
def profile_update():
    print('profile/update')
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
        if ('fname' in data) and data['fname'] != '':
            user.fname = data['fname']
        if ('lname' in data) and data['lname'] != '':
            user.lname = data['lname']
        if ('avatar' in data) and data['avatar'] != '':
            user.avatar = data['avatar']
        if ('address' in data) and data['address'] != '':
            user.address = data['address']
        if ('city' in data) and data['city'] != '':
            user.city = data['city']
        if ('state' in data) and data['state'] != '':
            user.state = data['state']
        if ('zipcode' in data) and data['zipcode'] != '':
            user.zipcode = data['zipcode']
        if ('phone' in data) and data['phone'] != '':
            user.phone = data['phone']
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

@app.route('/apis/profile/b_address', methods = ['POST']) # billing address
def b_address():
    print('profile/b_address')
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
        if ('address' in data) and data['address'] != '':
            user.address = data['address']
        if ('city' in data) and data['city'] != '':
            user.city = data['city']
        if ('state' in data) and data['state'] != '':
            user.state = data['state']
        if ('zipcode' in data) and data['zipcode'] != '':
            user.zipcode = data['zipcode']
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


@app.route('/apis/profile/s_address', methods = ['POST']) # shipping address
def s_address():
    print('profile/s_address')
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
        if ('s_address' in data) and data['s_address'] != '':
            user.s_address = data['s_address']
        if ('s_city' in data) and data['s_city'] != '':
            user.s_city = data['s_city']
        if ('s_state' in data) and data['s_state'] != '':
            user.s_state = data['s_state']
        if ('s_zipcode' in data) and data['s_zipcode'] != '':
            user.s_zipcode = data['s_zipcode']
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

@app.route('/apis/profile/changepass', methods = ['POST']) 
def profile_changepass():
    print('profile/changepass')
    data = {}
    keys  = ['token', 'oldpass', 'newpass']
    try:
        for key in keys:
            data[key] = get_request(key, None)        
        if data['token'] is None or data['token'] == '' or \
            data['oldpass'] is None or data['oldpass'] == '' or \
            data['newpass'] is None or data['newpass'] == '':
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
        oldpass = hashlib.md5(data['oldpass'].encode()).hexdigest()
        if not oldpass == user.password:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_match,
                'message': model.ResponseText.no_match,
            })
        user.password = hashlib.md5(data['newpass'].encode()).hexdigest()
        user.token =  b64encode(bytearray(user.email + ":" + user.password, 'utf-8')).decode('ascii')
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
