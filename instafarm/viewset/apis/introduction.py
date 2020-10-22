import os
import hashlib

from flask import request, send_from_directory
from instafarm import app
from datetime import datetime
from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict, allow_extention

@app.route('/apis/introduction/add', methods = ['POST'])
def introduction_add():
    print('introduction/add')
    data = {}
    keys  = ['title', 'subtitle', 'description', 'image']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['title'] is None or data['title'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        introduction = model.Introduction(data['title'])
        if data['subtitle'] and data['subtitle'] != '':
            introduction.subtitle = data['subtitle']
        if data['description'] and data['description'] != '':
            introduction.description = data['description']
        if data['image'] and data['image'] != '':
            introduction.image = data['image']
        model.add(introduction)
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


@app.route('/apis/introduction/getall', methods = ['POST'])
def introduction_getall():
    print('introduction/getall')
    try:
        results = [introduction.to_dict() for introduction in model.Introduction.get_all()]
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


@app.route('/apis/introduction/update', methods = ['POST'])
def introduction_update():
    print('introduction/update')
    data = {}
    try:
        data = get_request_dict()
        if data['id'] is None or data['id'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        introduction = model.Introduction.get_by_id(int(data['id']))
        if ('title' in data) and data['title'] != '':
            introduction.title = data['title']
        if ('subtitle' in data) and data['subtitle'] != '':
            introduction.subtitle = data['subtitle']
        if ('price' in data) and data['price'] != '':
            introduction.price = data['price']
        if ('description' in data) and data['description'] != '':
            introduction.description = data['description']
        if ('image' in data) and data['image'] != '':
            introduction.image = data['image']
        model.add(introduction)
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

@app.route('/apis/introduction/delete', methods = ['POST'])
def introduction_delete():
    print('introduction/delete')
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
        introduction = model.Introduction.get_by_id(int(data['id']))
        model.delete(introduction)
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

@app.route('/apis/introduction/uploadimage', methods = ['POST'])
def introduction_uploadimage():
    print('introduction/uploadimage')
    data = {}
    try:
        if 'image' not in request.files:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        file = request.files['image']
        if not file or file.filename == '' or not allow_extention(file.filename):
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        filename = datetime.now().strftime("%Y%m%d%H%M%S%f") + '.' + file.filename.rsplit('.', 1)[1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'introduction', filename))
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': filename
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/introduction/<filename>')
def introduction_file(filename):
    print('introduction/getfile')
    return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.join('introduction', filename))



