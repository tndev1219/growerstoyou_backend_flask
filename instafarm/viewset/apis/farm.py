import hashlib

from instafarm import app
from datetime import datetime
from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict

@app.route('/apis/farm/create', methods = ['POST'])
def farm_create():
    print('farm/create')
    data = {}
    try:
        data = get_request_dict()
        if not ('name' in data) or data['name'] == '' or \
            not ('address' in data) or data['address'] == '' or \
            not ('city' in data) or data['city'] == '' or \
            not ('state' in data) or data['state'] == '' or \
            not ('zipcode' in data) or data['zipcode'] == '' or \
            not ('link_phone' in data) or data['link_phone'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        farm = model.Farm(data['name'])
        farm.address = data['address']
        farm.city = data['city']
        farm.state = data['state']
        farm.zipcode = data['zipcode']
        farm.link_phone = data['link_phone']
        if ('ownerid' in data) and data['ownerid'] != '':
            farm.ownerid = data['ownerid']
        if ('photo' in data) and data['photo'] != '':
            farm.photo = data['photo']
        if ('lat' in data) and data['lat'] != '':
            farm.lat = data['lat']
        if ('lon' in data) and data['lon'] != '':
            farm.lon = data['lon']
        if ('link_url' in data) and data['link_url'] != '':
            farm.link_url = data['link_url']
        if ('status' in data) and data['status'] != '':
            farm.status = data['status']
        if ('employees' in data) and data['employees'] != '':
            farm.employees = data['employees']
     
        model.add(farm)
        model.commit()
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': farm.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/farm/getall', methods = ['POST'])
def farm_getall():
    print('farm/getall')
    try:
        results = [farm.to_dict() for farm in model.Farm.get_all()]
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

@app.route('/apis/farm/getbyid', methods = ['POST'])
def farm_getbyid():
    print('farm/getbyid')
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
        farm = model.Farm.get_by_id(data['farmid'])
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': farm.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/farm/update', methods = ['POST'])
def farm_update():
    print('farm/update')
    data = {}
    try:
        data = get_request_dict()
        if not ('id' in data) or data['id'] == '' or \
            not ('token' in data) or data['token'] == '':
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
        farm = model.Farm.get_by_id(data['id'])
        if ('name' in data) and data['name'] != '':
            farm.name = data['name']
        if ('ownerid' in data) and data['ownerid'] != '':
            farm.ownerid = data['ownerid']
        if ('photo' in data) and data['photo'] != '':
            farm.photo = data['photo']
        if ('address' in data) and data['address'] != '':
            farm.address = data['address']
        if ('city' in data) and data['city'] != '':
            farm.city = data['city']
        if ('state' in data) and data['state'] != '':
            farm.state = data['state']
        if ('zipcode' in data) and data['zipcode'] != '':
            farm.zipcode = data['zipcode']
        if ('lat' in data) and data['lat'] != '':
            farm.lat = data['lat']
        if ('lon' in data) and data['lon'] != '':
            farm.lon = data['lon']
        if ('link_url' in data) and data['link_url'] != '':
            farm.link_url = data['link_url']
        if ('link_phone' in data) and data['link_phone'] != '':
            farm.link_phone = data['link_phone']
        if ('status' in data) and data['status'] != '':
            farm.status = data['status']
        if ('employees' in data) and data['employees'] != '':
            farm.employees = data['employees']

        model.add(farm)
        model.commit()
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': farm.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/farm/delete', methods = ['POST']) # not in active
def farm_delete():
    print('farm/delete')
    data = {}
    keys = ['id']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['id'] is None or data['id'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        farm = model.Farm.get_by_id(data['id'])
        model.delete(farm)
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
