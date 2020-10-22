import json
import hashlib

from instafarm import app
from instafarm.models import model
from flask_mail import Message, Mail
from flask import Response, redirect, request, session

mail = Mail(app)

def send_mail(title, recipients, html='', text='', sender=None):
    
    if recipients is None:
        return True
    if not isinstance(recipients, list) and not isinstance(recipients, tuple):
        recipients = [recipients]
    msg = Message(subject=title, recipients=recipients)
    if sender is not None:
        msg.sender = sender
    msg.html = html
    msg.body = text
    # mail.send(msg)
    try:
        with mail.connect() as conn:
            conn.send(msg)
        return True
    except Exception as e:
        print(e)
        return False
    
    
def json_response(obj, status=200):
    return Response(
        json.dumps(obj),
        status=status,
        mimetype='application/json')

def get_request(key, default_value=None):
    if key is None or key == '':
        return default_value
    value = request.values.get(key)
    if value is None and request.is_json:
        json_values = request.get_json()
        if json_values is not None and key in json_values:
            value = json_values[key]
    if value is None:
        value = default_value
    return value 

def base_sign_in(user):
    if user is None:
        if 'me' in session:
            session.pop('me')
    else:
        session['me'] = user.to_dict()


def base_sign_out():
    if 'me' in session:
        session.pop('me')


def base_get_me():
    if 'me' in session and session['me'] is not None:
        return models.User.find_one_by_id(session['me']['id'])
    return None

# def is_admin(user):
#     if user is None:
#         return False
#     if isinstance(user, models.User):
#         return user.role == '0'

def get_request_dict():
    form_data = {}
    if request.is_json:
        form_data = request.get_json()
    elif request.form is not None:
        for key, value in request.form.items():
            if key.endswith('[]'):
                key = key[0:len(key) - 2]
                if key not in form_data:
                    form_data[key] = []
                elif not isinstance(form_data[key], list):
                    form_data[key] = [form_data[key]]
                form_data[key].append(value)
            else:
                if key not in form_data:
                    form_data[key] = value
                else:
                    if not isinstance(form_data[key], list):
                        form_data[key] = [form_data[key]]
                    form_data[key].append(form_data[key])
    query_data = {}
    if request.args is not None:
        for key, value in request.args.items():
            if key.endswith('[]'):
                key = key[0:len(key) - 2]
                if key not in query_data:
                    query_data[key] = []
                elif not isinstance(query_data[key], list):
                    query_data[key] = [query_data[key]]
                query_data[key].append(value)
            else:
                if key not in query_data:
                    query_data[key] = value
                else:
                    if not isinstance(query_data[key], list):
                        query_data[key] = [query_data[key]]
                    query_data[key].append(query_data[key])
    result = dict()
    result.update(form_data)
    result.update(query_data)
    return result

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        me = base_get_me()
        if me is None:
            return json_response({
                "success": False,
                "message": models.ErrorCodes.require_login
            })
        return f(*args, **kwargs)
    return decorated_function        

def allow_extention(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENTIONS']
