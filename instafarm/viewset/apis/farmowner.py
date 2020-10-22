import hashlib

from flask import request, session, render_template
from instafarm import app
from datetime import datetime
from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict, send_mail

@app.route('/apis/farmowner/add_farmer', methods = ['POST']) 
def farmowner_add_farmer():
    print('farmowner/add_farmer')
    data = {}
    try:
        data = get_request_dict()
        if not ('token' in data) or data['token'] == '' or \
            not ('farmid' in data) or data['farmid'] == '' or \
            not ('fname' in data) or data['fname'] == '' or \
            not ('lname' in data) or data['lname'] == '' or \
            not ('email' in data) or data['email'] == '' or \
            not ('phone' in data) or data['phone'] == '' or \
            not ('password' in data) or data['password'] == '':
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
        if model.User.check_exist_by_email(data['email']):
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.exist_email,
                'message': model.ResponseText.exist_email,
            })
        role = 3 # farmer
        password = hashlib.md5(data['password'].encode()).hexdigest()
        farmer = model.User(data['email'], password, role, data['fname'], data['lname'])
        farmer.phone = data['phone']
        farmer.farmid = data['farmid']
        isSend = send_mail('Email and Password', farmer.email, html=render_template('user_emailpassword.html', username=farmer.fname+' '+farmer.lname, email=farmer.email, password=data['password']))
        if not isSend:
            print('Send email failed.')
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.send_email_error,
                'message': model.ResponseText.send_email_error,
            })
        model.add(farmer)
        model.commit()
        model.refresh(farmer)
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : farmer.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })


@app.route('/apis/farmowner/get_farmers', methods = ['POST']) 
def farmowner_get_farmers():
    print('farmowner/get_farmers')
    data = {}
    try:
        data = get_request_dict()
        if not ('token' in data) or data['token'] == '' or \
            not ('farmid' in data) or data['farmid'] == '':
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
        role = 3 # farmer
        results = [farmer.to_dict() for farmer in model.User.get_by_role_and_farmid(role, data['farmid'])]
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


@app.route('/apis/farmowner/delete_farmer', methods = ['POST']) 
def farmowner_delete_farmer():
    print('farmowner/delete_farmer')
    data = {}
    try:
        data = get_request_dict()
        if not ('token' in data) or data['token'] == '' or \
            not ('farmerid' in data) or data['farmerid'] == '':
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
        farmer = model.User.find_by_id(data['farmerid'])
        model.delete(farmer)
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