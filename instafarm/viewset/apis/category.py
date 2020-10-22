import os
import hashlib

from flask import request, send_from_directory
from instafarm import app
from datetime import datetime
from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict, allow_extention


@app.route('/apis/pcategory/add', methods = ['POST'])
def pcategory_add():
    print('category/add')
    data = {}
    keys = ['name', 'image']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['name'] is None or data['name'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        if data['image'] is None or data['image'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        if model.PCategory.find_by_name(data['name']):
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.exist_error,
                'message': model.ResponseText.exist_error,
            })
        category = model.PCategory(data['name'])
        category.image = data['image']
        model.add(category)
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

@app.route('/apis/pcategory/uploadimage', methods = ['POST'])
def category_uploadimage():
    print('category/uploadimage')
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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'category', filename))
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


@app.route('/apis/pcategory/getall', methods = ['POST'])
def pcategory_getall():
    print('category/getall')
    try:
        results = [category.to_dict() for category in model.PCategory.get_all()]
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


@app.route('/apis/pcategory/update', methods = ['POST'])
def pcategory_update():
    print('category/update')
    data = {}
    keys = ['id', 'name', 'image']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['id'] is None or data['id'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        category = model.PCategory.get_by_id(int(data['id']))
        if data['name'] and data['name'] != '':
            category.name = data['name']
        if data['image'] and data['image'] != '':
            category.image = data['image']
        model.add(category)
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

@app.route('/apis/pcategory/delete', methods = ['POST']) # not in active
def pcategory_delete():
    print('category/delete')
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
        category = model.PCategory.get_by_id(int(data['id']))
        model.delete(category)
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

@app.route('/category/<filename>')
def category_file(filename):
    print('category/getfile')
    return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.join('category', filename))