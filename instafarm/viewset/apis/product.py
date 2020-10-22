import os
import hashlib

from flask import request, send_from_directory
from instafarm import app
from datetime import datetime
from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict, allow_extention

@app.route('/apis/product/add', methods = ['POST'])
def product_add():
    print('product/add')
    data = {}
    keys  = ['name', 'unit', 'price', 'description', 'count', 'farmid', 'categoryid', 'images']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['name'] is None or data['name'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        # if model.Product.find_by_name(data['name']):
        #     return json_response({
        #         'success': False,
        #         'errcode': model.ResponseCode.exist_error,
        #         'message': model.ResponseText.exist_error,
        #     })
        product = model.Product(data['name'], data['unit'], float(data['price']), int(data['count']), data['description'])
        product.images = str(data['images'])
        product.categoryid = data['categoryid']
        product.farmid = data['farmid']
        model.add(product)
        model.commit()
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': product.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/product/getall', methods = ['POST'])
def product_getall():
    print('product/getall')
    data = get_request_dict()
    try:
        results = [product.to_dict() for product in model.Product.get_all()]
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

@app.route('/apis/product/getbyid', methods = ['POST'])
def product_getbyid():
    print('product/getbyid')
    data = {}
    keys  = ['id']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['id'] is None or data['id'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        results = model.Product.get_by_id(int(data['id'])).to_dict() 
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
    
@app.route('/apis/product/getbyfarmid', methods = ['POST'])
def product_getbyfarmid():
    print('product/getbyfarmid')
    data = {}
    keys  = ['farmid']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['farmid'] is None or data['farmid'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        results = [product.to_dict() for product in model.Product.get_by_farmid(int(data['farmid']))]
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

@app.route('/apis/product/getbyparam', methods = ['POST'])
def product_getbyparam():
    print('admin/getbyparam')
    data = get_request_dict()
    try:
        if not ('ids' in data) or data['ids'] == '' or \
            not ('lower_price' in data) or data['lower_price'] == '' or \
            not ('upper_price' in data) or data['upper_price'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        if not ('keyword' in data) or data['keyword'] == '':
            data['keyword'] = ''
        results = [product.to_dict() for product in model.Product.getbyparam(data['ids'], data['lower_price'], data['upper_price'], data['keyword'])]
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

@app.route('/apis/product/update', methods = ['POST'])
def product_update():
    print('product/update')
    data = {}
    try:
        data = get_request_dict()
        if data['id'] is None or data['id'] == '':
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.bad_param,
                'message': model.ResponseText.bad_param,
            })
        product = model.Product.get_by_id(data['id'])
        if ('name' in data) and data['name'] != '':
            product.name = data['name']
        if ('unit' in data) and data['unit'] != '':
            product.unit = data['unit']
        if ('price' in data) and data['price'] != '':
            product.price = data['price']
        if ('description' in data) and data['description'] != '':
            product.description = data['description']
        if ('count' in data) and data['count'] != '':
            product.count = data['count']
        if ('farmid' in data) and data['farmid'] != '':
            product.farmid = data['farmid']
        if ('categoryid' in data) and data['categoryid'] != '':
            product.categoryid = data['categoryid']
        if ('images' in data) and data['images'] != '':
            product.images = str(data['images'])
        model.add(product)
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

@app.route('/apis/product/delete', methods = ['POST'])
def product_delete():
    print('product/delete')
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
        product = model.Product.get_by_id(data['id'])
        product.status = 1
        model.add(product)
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

@app.route('/apis/product/uploadimage', methods = ['POST'])
def product_uploadimage():
    print('product/uploadimage')
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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'products', filename))
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

@app.route('/product/<filename>')
def product_file(filename):
    print('product/getfile')
    return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.join('products', filename))



