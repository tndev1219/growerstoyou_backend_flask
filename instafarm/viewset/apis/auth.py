import hashlib

from flask import request, session, render_template
from instafarm import app
from datetime import datetime
from instafarm.models import model
from base64 import b64encode, b64decode
from instafarm.viewset.base import json_response, get_request, get_request_dict, send_mail


@app.route('/apis/signup', methods = ['POST']) # sign up
def signup():
    print('auth/signup')
    data = {}
    # keys = ['email', 'password', 'role', 'address', 'avatar', 'city', 'fname', 'lat', 'lname', 'lon', 'membership', 'phone', 'state', 'username', 'zipcode',
    #         # driver
    #         'license_id', 'license_image', 'license_number', 'vehicle_type', 'vehicle_image', 'vehicle_number', 'issued_date', 'expired_date'] 
    try: 
        data = get_request_dict()
        
        if not ('role' in data) or data['role'] == '' or \
            not ('email' in data) or data['email'] == '' or \
            not ('password' in data) or data['password'] == '' or \
            not ('fname' in data) or data['fname'] == '' or \
            not ('lname' in data) or data['lname'] == '' or \
            not ('address' in data) or data['address'] == '' or \
            not ('city' in data) or data['city'] == '' or \
            not ('state' in data) or data['state'] == '' or \
            not ('zipcode' in data) or data['zipcode'] == '' or \
            not ('baseurl' in data) or data['baseurl'] == '' or \
            not ('phone' in data) or data['phone'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        if model.User.check_exist_by_email(data['email']):
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.exist_email,
                'message': model.ResponseText.exist_email,
            })
        role = int(data['role'])
        baseurl = data['baseurl']
        password = hashlib.md5(data['password'].encode()).hexdigest()
        user = model.User(data['email'], password, role, data['fname'], data['lname'])
        # 0:admin, 1: customer, 2: farmer-admin, 3: farmer, 4: driver
        if role == 2: # farm owner
            print('Farm Owner')
            if not ('farm_name' in data) or data['farm_name'] == '' or \
                not ('farm_address' in data) or data['farm_address'] == '' or \
                not ('farm_city' in data) or data['farm_city'] == '' or \
                not ('farm_state' in data) or data['farm_state'] == '' or \
                not ('farm_zipcode' in data) or data['farm_zipcode'] == '' or \
                not ('farm_link_phone' in data) or data['farm_link_phone'] == '':
                return json_response({
                    'success': False,
                    'errcode': model.ResponseCode.bad_param,
                    'message': model.ResponseText.bad_param,
                })
            farm = model.Farm(data['farm_name'])
            farm.address = data['farm_address']
            farm.city = data['farm_city']
            farm.state = data['farm_state']
            farm.zipcode = data['farm_zipcode']
            farm.link_phone = data['farm_link_phone']
            if ('farm_photo' in data) and data['farm_photo'] != '':
                farm.photo = data['farm_photo']
            if ('farm_lat' in data) and data['farm_lat'] != '':
                farm.lat = data['farm_lat']
            if ('farm_lon' in data) and data['farm_lon'] != '':
                farm.lon = data['farm_lon']
            if ('farm_link_url' in data) and data['farm_link_url'] != '':
                farm.link_url = data['farm_link_url']
            if ('farm_status' in data) and data['farm_status'] != '':
                farm.status = data['farm_status']
            if ('farm_employees' in data) and data['farm_employees'] != '':
                farm.employees = data['farm_employees']
            model.add(farm)
            model.commit()
            model.refresh(farm)
            user.farmid = farm.id
        if role == 4: # driver
            print('Driver Sign up')
            if not ('license_id' in data) or data['license_id'] == '' or \
                not ('license_number' in data) or data['license_number'] == '' or \
                not ('issued_date' in data) or data['issued_date'] == '' or \
                not ('expired_date' in data) or data['expired_date'] == '' or \
                not ('driver_address' in data) or data['driver_address'] == '' or \
                not ('driver_city' in data) or data['driver_city'] == '' or \
                not ('driver_state' in data) or data['driver_state'] == '' or \
                not ('driver_zipcode' in data) or data['driver_zipcode'] == '':
                return json_response({
                    'success': False,
                    'errcode': model.ResponseCode.bad_param,
                    'message': model.ResponseText.bad_param,
                })
            driver = model.Driver()
            driver.license_id = data['license_id']
            driver.license_number = data['license_number']
            driver.issued_date = data['issued_date']
            driver.expired_date = data['expired_date']
            driver.address = data['driver_address']
            driver.city = data['driver_city']
            driver.state = data['driver_state']
            driver.zipcode = data['driver_zipcode']
            driver.status = 0
            if ('license_image' in data) and data['license_image'] != '':
                driver.license_image = data['license_image']
            if ('vehicle_type' in data) and data['vehicle_type'] != '':
                driver.vehicle_type = data['vehicle_type']
            if ('vehicle_image' in data) and data['vehicle_image'] != '':
                driver.vehicle_image = data['vehicle_image']
            if ('vehicle_number' in data) and data['vehicle_number'] != '':
                driver.vehicle_number = data['vehicle_number']
            model.add(driver)
            model.commit()
            model.refresh(driver)
            user.driverid = driver.id
        user.phone = data['phone']
        user.address = data['address']
        user.city = data['city']
        user.state = data['state']
        user.zipcode = data['zipcode']
        model.add(user)
        model.commit()
        model.refresh(user)
        if role == 2:
            farm = model.Farm.get_by_id(user.farmid)
            farm.ownerid = user.id
            model.add(farm)
            model.commit()
        isSend = send_mail('Email Confirm', user.email, html=render_template('user_confirm.html', username=user.fname+' '+user.lname, server=baseurl, token=user.token))
        if not isSend:
            print('Send email failed.')
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': user.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/confirm/email', methods = ['POST'])
def confirm_email():
    print('auth/confirm_email')
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
        user.email_verify = True
        model.add(user)
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

@app.route('/apis/signin', methods = ['POST'])
def signin():
    print('auth/siginin')
    data = {}
    keys = ['email', 'password']
    try: 
        for key in keys:
            data[key] = get_request(key, None)
        password = hashlib.md5(data['password'].encode()).hexdigest()
        user = model.User.find_by_email_and_password(data['email'], password)
        if not user:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.auth_error,
                'message': model.ResponseText.auth_error,
            })
        # if not user.email_verify:
        #     return json_response({
        #     'success': False,
        #     'errcode': model.ResponseCode.require_email_verify,
        #     'message': model.ResponseText.require_email_verify,
        # })
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : user.to_dict(),
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/forgotpass', methods = ['POST'])
def forgotpass():
    print('auth/forgotpass')
    data = {}
    keys  = ['email', 'baseurl']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['email'] is None or data['email'] == '' or \
            data['baseurl'] is None or data['baseurl'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        email = data['email']
        baseurl = data['baseurl']
        user = model.User.find_by_email(data['email'])
        if not user:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        isSend = send_mail('Forgot Password', user.email, html=render_template('user_forgotpass.html', username=user.fname+' '+user.lname, server=baseurl, token=user.token))
        if not isSend:
            print('Send email failed.')
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

@app.route('/apis/resetpass', methods = ['POST'])
def resetpass():
    print('auth/resetpass')
    data = {}
    keys  = ['token', 'password']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['token'] is None or data['token'] == '' or \
            data['password'] is None or data['password'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_email,
                'message': model.ResponseText.bad_email,
            })
        user = model.User.find_by_token(data['token'])
        if not user:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        user.password = hashlib.md5(data['password'].encode()).hexdigest()
        user.token =  b64encode(bytearray(user.email + ":" + user.password, 'utf-8')).decode('ascii')
        model.add(user)
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


