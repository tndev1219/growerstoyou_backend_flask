import hashlib
import stripe

from flask import request, session, render_template
from instafarm import app
from datetime import datetime

from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict, send_mail

stripe.api_key = app.config['STRIP_SECRET_KEY']

@app.route('/apis/order/add', methods = ['POST']) 
def order_add():
    print('order/add')
    data = {}
    try:
        data = get_request_dict()

        if not ('token' in data) or data['token'] == '' or \
            not ('basketids' in data) or data['basketids'] == '' or \
            not ('customerid' in data) or data['customerid'] == '' or \
            not ('fname' in data) or data['fname'] == '' or \
            not ('lname' in data) or data['lname'] == '' or \
            not ('email' in data) or data['email'] == '' or \
            not ('phone' in data) or data['phone'] == '' or \
            not ('address' in data) or data['address'] == '' or \
            not ('city' in data) or data['city'] == '' or \
            not ('state' in data) or data['state'] == '' or \
            not ('zipcode' in data) or data['zipcode'] == '':
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
        farmids = []
        totalprice = 0

        baskets = model.Basket.get_by_ids(data['basketids'])
        for basket in baskets:
            if not basket.productinfo.farmid in farmids:
                farmids.append(basket.productinfo.farmid)
        for farmid in farmids:
            basketids = []
            productcost = 0
            shipmentcost= 0
            paymentcost = 0
            order = model.Order()
            order.userid = user.id 
            order.farmid = farmid
            order.fname = data['fname']
            order.lname = data['lname']
            order.address = data['address']
            order.city = data['city']
            order.state = data['state']
            order.zipcode = data['zipcode']
            order.email = data['email']
            order.phone = data['phone']
            order.status = 0
            for basket in baskets:
                if farmid == basket.productinfo.farmid:
                    basketids.append(basket.id)
                    productcost += int(basket.count)* float(basket.productinfo.price)
                    
            paymentcost = productcost + shipmentcost
            # totalprice += paymentcost
            order.basketids = str(basketids)
            order.productcost = productcost
            order.shipmentcost= shipmentcost
            order.paymentcost = paymentcost
            try:
                stripe.Charge.create(
                    customer=data['customerid'],
                    amount=int(paymentcost*100),
                    currency='usd',
                    description='Flask Charge'
                )
                for basket in baskets:
                    if farmid == basket.productinfo.farmid:
                        basket.buyunit  = basket.productinfo.unit
                        basket.buyprice = basket.productinfo.price 
                        basket.status = 1
                        model.add(basket)
                        model.commit()
                        product = model.Product.get_by_id(basket.productinfo.id)
                        product.count -= basket.count
                        model.add(product)
                        model.commit()
            except stripe.error.StripeError:
                return json_response({
                    'success': False,
                    'errcode': model.ResponseCode.pay_error,
                    'message': model.ResponseText.pay_error,
                })
            model.add(order)
            model.commit()
            model.refresh(order)

            farm = model.Farm.get_by_id(farmid)
        
            transaction = model.Transaction()
            transaction.userid = user.id
            transaction.orderid = order.id
            transaction.farmid = farmid
            transaction.farmname = farm.name
            transaction.basketids = str(basketids)
            transaction.amount = paymentcost
            transaction.customerid = data['customerid']
            transaction.customername = data['fname'] + ' ' + data['lname']
            transaction.currency = 'usd'
            model.add(transaction)
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

@app.route('/apis/order/getall', methods = ['POST'])
def order_getall():
    print('order/getall')
    data = {}
    keys = ['token', 'offset', 'limit']
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
        offset = 0
        limit  = 50000
        
        if ('offset' in data) and data['offset'] != '':
            offset = int(data['offset'])
        if ('limit' in data) and data['limit'] != '':
            limit = int(data['limit'])
        orders = model.Order.get_all(offset, limit)['data']
        results = []
        no = 1
        for order in orders:
            result = order.to_dict()
            result['no'] = no
            results.append(result)
            no += 1
        # results = [order.to_dict() for order in orders]
        allcount = model.Order.get_all(offset, limit)['count']
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': results,
            'allcount': allcount
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/order/getbyuserid', methods = ['POST'])
def order_getbyuserid():
    print('order/getbyuserid')
    data = {}
    keys = ['token', 'userid', 'offset', 'limit', 'keyword']
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
        user = model.User.find_by_token(data['token'])
        if not user:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        offset = 0
        limit  = 50000
        keyword = ''
        
        if ('offset' in data) and data['offset'] != '':
            offset = int(data['offset'])
        if ('limit' in data) and data['limit'] != '':
            limit = int(data['limit'])
        if ('keyword' in data) and data['keyword'] != '':
            keyword = data['keyword']
        orders = model.Order.get_by_userid(data['userid'], offset, limit, keyword)['data']
        print('success')
        results = []
        no = 1
        for order in orders:
            result = order.to_dict()
            result['no'] = no
            results.append(result)
            no += 1
        # results = [order.to_dict() for order in orders]
        allcount = model.Order.get_by_userid(data['userid'], offset, limit, keyword)['count']
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': results,
            'allcount': allcount
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/order/getbyfarmid', methods = ['POST'])
def order_getbyfarmid():
    print('order/getbyfarmid')
    data = {}
    keys = ['token', 'farmid', 'offset', 'limit', 'keyword']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['farmid'] is None or data['farmid'] == '' or \
            data['token'] is None or data['token'] == '':
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
        offset = 0
        limit  = 50000
        keyword = ''
        
        if ('offset' in data) and data['offset'] != '':
            offset = int(data['offset'])
        if ('limit' in data) and data['limit'] != '':
            limit = int(data['limit'])
        if ('keyword' in data) and data['keyword'] != '':
            keyword = data['keyword']
        print(keyword)
        orders = model.Order.get_by_farmid(data['farmid'], offset, limit, keyword)['data']
        results = []
        no = 1
        for order in orders:
            result = order.to_dict()
            result['no'] = no
            results.append(result)
            no += 1
        # results = [order.to_dict() for order in orders]
        allcount = model.Order.get_by_farmid(data['farmid'], offset, limit, keyword)['count']
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': results,
            'allcount': allcount
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/order/detail', methods = ['POST'])
def order_detail():
    print('order/detail')
    data = {}
    keys = ['token', 'orderid']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['orderid'] is None or data['orderid'] == '' or \
            data['token'] is None or data['token'] == '':
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
        
        order = model.Order.get_by_id(data['orderid'])
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results': order.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })


@app.route('/apis/order/delete', methods = ['POST'])
def order_delete():
    print('order/delete')
    data = {}
    keys = ['token','orderid']
    try:
        for key in keys:
            data[key] = get_request(key, None)
        if data['orderid'] is None or data['orderid'] == '' or \
            data['token'] is None or data['token'] == '':
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
        order = model.Order.get_by_id(int(data['orderid']))
        model.delete(order)
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

@app.route('/apis/order/search', methods = ['POST'])
def order_search():
    print('order/search')
    data = get_request_dict()
    try:
        if  not ('token' in data) or data['token'] == '':
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
        if not ('keyword' in data) or data['keyword'] == '':
            data['keyword'] = ''
        results = [order.to_dict() for order in model.Order.search(data['keyword'])]
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
