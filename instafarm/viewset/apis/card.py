import hashlib
import stripe

from flask import request, session, render_template
from instafarm import app
from datetime import datetime
from instafarm.models import model
from instafarm.viewset.base import json_response, get_request, get_request_dict, send_mail

stripe.api_key = app.config['STRIP_SECRET_KEY']

@app.route('/apis/card/add', methods = ['POST']) 
def card_add():
    print('card/add')
    data = {}
    try:
        data = get_request_dict()

        if not ('token' in data) or data['token'] == '' or \
            not ('stripetoken' in data) or data['stripetoken'] == '' or \
            not ('number' in data) or data['number'] == '' or \
            not ('funding' in data) or data['funding'] == '' or \
            not ('branch' in data) or data['branch'] == '':
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
        card = model.Card()
        card.userid = user.id
        card.branch = data['branch']
        card.number = data['number']
        card.funding = data['funding']
        try:
            customer = stripe.Customer.create(
                email  = user.email,
                source = data['stripetoken']
            )
            card.customerid = customer.id
        except stripe.error.StripeError:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.pay_error,
                'message': model.ResponseText.pay_error,
            })
        model.add(card)
        model.commit()
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : card.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/card/getall', methods = ['POST']) 
def card_getall():
    print('card/getall')
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
        
        results = [card.to_dict() for card in model.Card.get_all()]
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

@app.route('/apis/card/usercard', methods = ['POST']) 
def card_usercard():
    print('card/usercard')
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
        
        results = [card.to_dict() for card in model.Card.card_by_token(data['token'])]
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

@app.route('/apis/card/getbyid', methods = ['POST']) 
def card_getbyid():
    print('card/getbyid')
    data = {}
    try:
        data = get_request_dict()
        if not ('token' in data) or data['token'] == '' or \
            not ('cardid' in data) or data['cardid'] == '':
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
        
        card = model.Card.get_by_id(data['cardid'])
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : card.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/card/update', methods = ['POST'])
def card_update():
    print('card/update')
    data = {}
    try:
        data = get_request_dict()
        if not ('token' in data) or data['token'] == '' or \
            not ('stripetoken' in data) or data['stripetoken'] == '' or \
            not ('cardid' in data) or data['cardid'] == '': \
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
        card = model.Card.get_by_id(data['cardid'])
        if not card:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        try:
            customer = stripe.Customer.create(
                email  = user.email,
                source = data['stripetoken']
            )
            card.customerid = customer.id
        except stripe.error.StripeError:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.pay_error,
                'message': model.ResponseText.pay_error,
            })

        if ('branch' in data) and data['branch'] != '':
            card.branch = data['branch']
        if ('number' in data) and data['number'] != '':
            card.number = data['number']
        if ('funding' in data) and data['funding'] != '':
            card.funding = data['funding']

        model.add(card)
        model.commit()
        return json_response({
            'success': True,
            'message': model.ResponseText.success,
            'results' : card.to_dict()
        })
    except:
        return json_response({
            'success': False,
            'errcode': model.ResponseCode.server_error,
            'message': model.ResponseText.server_error,
        })

@app.route('/apis/card/delete', methods = ['POST'])
def card_delete():
    print('card/delete')
    data = {}
    try:
        data = get_request_dict()
        if not ('token' in data) or data['token'] == '' or \
            not ('cardid' in data) or data['cardid'] == '':
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
        card = model.Card.get_by_id(data['cardid'])
        if not card:
            return json_response({
                'success': False,
                'errcode': model.ResponseCode.no_exist,
                'message': model.ResponseText.no_exist,
            })
        model.delete(card)
        model.commit()
        results = [card.to_dict() for card in model.Card.get_all()]
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

