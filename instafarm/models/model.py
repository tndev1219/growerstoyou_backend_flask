import ast
from datetime import datetime
from base64 import b64encode, b64decode
from instafarm import app, db
from sqlalchemy.orm import backref
from sqlalchemy import desc

def commit():
    db.session.commit()

def rollback():
    db.session.rollback()

def add(model):
    db.session.add(model)

def delete(model):
    db.session.delete(model)

def refresh(model):
    db.session.refresh(model)

def clear():
    db.session.clear()


class ResponseText:
    # success
    success       = 'SUCCESS'
    # error
    server_error  = 'SERVER ERROR'
    auth_error    = 'AUTH ERROR'
    inactive_user = 'INACTIVE USER'
    expired_user  = 'EXPIRED USER'
    deleted_user  = 'DELETED USER'
    blocked_user  = 'BLOCKED USER'
    bad_email     = 'BAD EMAIL'
    bad_password  = 'BAD PASSWORD'
    exist_email   = 'EMAIL EXIST'
    exist_error   = 'ALEADY EXIST'
    bad_role      = 'BAD ROLE'
    bad_param     = 'BAD PARAMETERS'
    require_login = 'LOGIN REQUIRE'
    require_email_verify = 'EMAIL NOT VERIFIED'
    bad_request = 'BAD REQUEST'
    no_exist = 'NO EXIST'
    beyond = 'AMOUNT GOES BEYOND MAX VALUE'
    pay_error = 'PAY ERROR'
    no_match = 'NOT MATCH'
    send_email_error = 'SEND EMAIL ERROR'

class ResponseCode:
    # success
    success       = 200
    # error
    server_error  = 404
    auth_error    = 403
    inactive_user = 405
    expired_user  = 406
    deleted_user  = 407
    blocked_user  = 408
    exist_email   = 409
    exist_error   = 410
    bad_email     = 411
    bad_password  = 412
    bad_role      = 413
    bad_param     = 414
    require_login = 415
    require_email_verify = 416
    bad_request = 417
    no_exist = 418
    beyond = 419
    pay_error = 501
    no_match = 502
    send_email_error = 503

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email    = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role     = db.Column(db.Integer, nullable=False) # 0:admin, 1: customer, 2: farm-onwer, 3: farmer,  4: driver
    fname    = db.Column(db.String(100), nullable=True)
    lname    = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), unique=True)
    phone    = db.Column(db.String(100))
    avatar   = db.Column(db.String(256))
    address  = db.Column(db.String(256))
    city     = db.Column(db.String(256))
    state    = db.Column(db.String(256))
    zipcode  = db.Column(db.String(100))
    s_address  = db.Column(db.String(256)) # shipping address
    s_city     = db.Column(db.String(256))
    s_state    = db.Column(db.String(256))
    s_zipcode  = db.Column(db.String(100))
    lat      = db.Column(db.Float)
    lon      = db.Column(db.Float)
    status   = db.Column(db.String(10))  # 0: inactive, 1: active, 2: block, 3: expired, 4: delete
    token    = db.Column(db.String(256))
    membership   = db.Column(db.String(100))
    email_verify = db.Column(db.Boolean)
    phone_verify = db.Column(db.Boolean)
    expired_date = db.Column(db.DateTime)

    driverid   = db.Column('driverid', db.Integer, db.ForeignKey('drivers.id'))
    driverinfo = db.relationship('Driver', backref=backref('drivers', lazy=True, uselist=True))

    farmid   = db.Column('farmid', db.Integer, db.ForeignKey('farms.id'))
    farminfo = db.relationship('Farm', backref=backref('farms', lazy=True, uselist=True))

    create_at    = db.Column(db.DateTime)
    update_at    = db.Column(db.DateTime)

    def __init__(self, email='', password='', role=1, fname='', lname=''):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.role = role
        self.token =  b64encode(bytearray(email + ":" + password, 'utf-8')).decode('ascii')
        self.email_verify = False
        self.phone_verify = False
        self.status = 0 # inactive
        self.create_at = datetime.now()
        self.update_at = datetime.now()
    
    def get_token(self):
        return b64encode(bytearray(self.email + ":" + self.password, 'utf-8')).decode('ascii')
    
    def to_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'username': self.username,
            'phone': self.phone,
            'avatar': self.avatar,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            's_address': self.s_address,
            's_city': self.s_city,
            's_state': self.s_state,
            's_zipcode': self.s_zipcode,
            'role': self.role,
            'status': self.status,
            'lat': self.lat,
            'lon': self.lon,
            'memebership': self.membership,
            'email_verify': self.email_verify,
            'phone_verify': self.phone_verify,
            'expired_date': self.expired_date,
            'create_at': str(self.create_at),
            'update_at': str(self.update_at),
            'driverinfo': {
                'driver_id': self.driverinfo.id, 
                'license_id': self.driverinfo.license_id, 
                'license_image': self.driverinfo.license_image,
                'license_number': self.driverinfo.license_number,
                'vehicle_type': self.driverinfo.vehicle_type,
                'vehicle_image': self.driverinfo.vehicle_image,
                'vehicle_number': self.driverinfo.vehicle_number,
                'issued_date': str(self.driverinfo.issued_date),
                'expired_date': str(self.driverinfo.expired_date),
                'address': self.driverinfo.address,
                'city': self.driverinfo.city,
                'state': self.driverinfo.state,
                'zipcode': self.driverinfo.zipcode,
                'status': self.driverinfo.status
                # 'create_at': self.driverinfo.create_at,
                # 'update_at': self.driverinfo.update_at,
            } if self.driverinfo else None,
            'farminfo': {
                'farm_id': self.farminfo.id,
                'ownerid': self.farminfo.ownerid, 
                'name': self.farminfo.name,
                'photo': self.farminfo.photo,
                'address': self.farminfo.address,
                'city': self.farminfo.city,
                'state': self.farminfo.state,
                'zipcode': self.farminfo.zipcode,
                'lat': self.farminfo.lat,
                'lon': self.farminfo.lon,
                'link_url': self.farminfo.link_url,
                'link_phone': self.farminfo.link_phone,
                'employees': self.farminfo.employees,
                'status': self.farminfo.status,
                # 'create_at': self.farminfo.create_at,
                # 'update_at': self.farminfo.update_at,
            } if self.farminfo else None,
        }
    
    @staticmethod
    def find_by_id(uid):
        return User.query.get(uid)
   
    @staticmethod
    def get_by_role(role):
        if role is None or role == '':
            return None
        return User.query.filter_by(role=role).all()
    
    @staticmethod
    def get_by_role_status(role, status):
        if role is None or role == '':
            return None
        if status is None or status == '':
            return None
        return User.query.filter_by(role=role, status=status).all()
    
    @staticmethod
    def find_by_email(email):
        if email is None or email == '':
            return None
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def auth_by_token(token):
        if token is None or token == '':
            return None
        return User.query.filter_by(token=token).first()

    @staticmethod
    def find_by_token(token):
        try:
            decoded_token = b64decode(bytearray(token, "ascii")).decode('utf-8')
            print(decoded_token)
            tokens = decoded_token.split(":")
            email = tokens[0]
            password = tokens[1]
            return User.find_by_email_and_password(email, password)
        except:
            return []

    @staticmethod
    def auth_by_token(token):
        if token is None or token == '':
            return None
        return User.query.filter_by(token=token).first()
    
    @staticmethod
    def find_by_email(email):
        if email is None or email == '':
            return None
        return User.query.filter_by(email=email).first()    
    
    @staticmethod
    def find_by_email_and_password(email, password):
        if email is None or email == '':
            return None
        if password is None or password == '':
            return None
        return User.query.filter_by(email=email, password=password).first()
    
    @staticmethod
    def get_by_role_and_farmid(role, farmid):
        if role is None or role == '':
            return None
        if farmid is None or farmid == '':
            return None
        return User.query.filter_by(role=role, farmid=farmid).all()
    
    @staticmethod
    def check_exist_by_email(email, me=None):
        user = User.query.filter_by(email=email).first()
        if user is None:
            return False
        if me is None:
            return True
        return me.id != user.id

class Driver(db.Model):
    __tablename__ = 'drivers'

    id  = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    license_id     =  db.Column(db.String(100))
    license_image  = db.Column(db.String(256))
    license_number = db.Column(db.String(100))
    vehicle_type   = db.Column(db.String(100))
    vehicle_image  = db.Column(db.String(256))
    vehicle_number = db.Column(db.String(100))
    issued_date    = db.Column(db.DateTime)
    expired_date   = db.Column(db.DateTime)
    address  = db.Column(db.String(100))
    city     = db.Column(db.String(100))
    state    = db.Column(db.String(100))
    zipcode  = db.Column(db.String(100))
    status   = db.Column(db.Integer)
    create_at      = db.Column(db.DateTime)
    update_at      = db.Column(db.DateTime)

    def __init__(self):
        self.create_at = datetime.now()
        self.update_at = datetime.now()

    @staticmethod
    def get_by_userid(userid):
        if userid is None or userid == '':
            return None
        return Driver.query.filter_by(userid=userid).first()     
    
class Farm(db.Model):
    __tablename__ = 'farms'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    ownerid = db.Column(db.Integer)
    # ownerid   = db.Column('ownerid', db.Integer, db.ForeignKey('users.id'))
    ownerinfo = db.relationship('User', backref=backref('users', lazy=True, uselist=True))
    name      = db.Column(db.String(100), nullable=False)
    photo     = db.Column(db.String(256))
    address   = db.Column(db.String(256))
    city      = db.Column(db.String(100))
    state     = db.Column(db.String(100))
    zipcode   = db.Column(db.String(100))
    lat       = db.Column(db.Float)
    lon       = db.Column(db.Float)
    link_url  = db.Column(db.String(256))
    link_phone = db.Column(db.String(256))
    employees  = db.Column(db.String(256))
    status   = db.Column(db.Integer)
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __init__(self, name=''):
        self.name    = name
        self.create_at = datetime.now()
        self.update_at = datetime.now()

    @staticmethod
    def get_by_ownerid(ownerid):
        if uid is None or uid == '':
            return None
        return Farm.query.filter_by(ownerid=ownerid).first() 
    
    @staticmethod
    def get_by_id(id):
        if id is None or id == '':
            return None
        return Farm.query.filter_by(id=id).first() 
    
    @staticmethod
    def get_by_name(name):
        if name is None or name == '':
            return None
        return Farm.query.filter_by(name=name).first()

    @staticmethod
    def get_all():
        return Farm.query.all()
    
    def to_dict(self):
        return {
            'id': self.id,
            'ownerid': self.ownerid,
            'ownerinfo': {
                # 'owner_id': self.ownerinfo.id, 
                # 'onwer_name': self.ownerinfo.name
            } if self.ownerinfo else None,
            'name' : self.name,
            'photo' : self.photo,
            'address': self.address,
            'city': self.city,
            'state' : self.state,
            'zipcode' : self.zipcode,
            'lat' : self.lat,
            'lon' : self.lon,
            'link_url' : self.link_url,
            'link_phone' : self.link_phone,
            'employees' : self.employees,
            'status' : self.status,
        }

class Introduction(db.Model): # introduction category 
    __tablename__ = 'introductions'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title       = db.Column(db.Text)
    subtitle    = db.Column(db.Text)
    description = db.Column(db.Text)
    image       = db.Column(db.String(5000))
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __init__(self, title=''):
        self.title    = title
        self.create_at = datetime.now()
        self.update_at = datetime.now()
    
    def to_dict(self):
        return {
            'id'  : self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'description': self.description,
            'image': self.image
        }

    @staticmethod
    def get_by_id(id):
        if id is None or id == '':
            return None
        return Introduction.query.filter_by(id=id).first() 

    @staticmethod
    def get_all():
        return Introduction.query.all()


class PCategory(db.Model): # product category 
    __tablename__ = 'pcategories'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name      = db.Column(db.String(256), nullable=False)
    image    = db.Column(db.String(5000))
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __init__(self, name=''):
        self.name    = name
        self.create_at = datetime.now()
        self.update_at = datetime.now()
    
    def to_dict(self):
        return {
            'id'  : self.id,
            'name': self.name,
            'image': self.image
        }

    @staticmethod
    def get_by_id(id):
        if id is None or id == '':
            return None
        return PCategory.query.filter_by(id=id).first() 
    
    @staticmethod
    def find_by_name(name):
        if name is None or name == '':
            return False
        category = PCategory.query.filter_by(name=name).first()
        if category is None:
            return False
        else:
            return True

    @staticmethod
    def get_all():
        return PCategory.query.all()
    


class Product(db.Model): # product list 
    __tablename__ = 'products'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    farmid    = db.Column('farmid', db.Integer, nullable=False)
    categoryid= db.Column('categoryid', db.Integer, db.ForeignKey('pcategories.id'))
    category  = db.relationship('PCategory', backref=backref('pcategories', lazy=True, uselist=True))
    name      = db.Column(db.String(256), nullable=False)
    unit      = db.Column(db.String(100))
    price     = db.Column(db.Float)
    description = db.Column(db.Text)
    count     = db.Column(db.Integer)
    status    = db.Column(db.Integer)
    images    = db.Column(db.String(5000))
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __init__(self, name='', unit='', price=0, count=0, description=''):
        self.name  = name
        self.unit  = unit
        self.price = price
        self.count = count
        self.status = 0
        self.description = description
        self.create_at = datetime.now()
        self.update_at = datetime.now()
    
    def to_dict(self):
        farm = None
        if (self.farmid):
            farm = Farm.query.filter_by(id=self.farmid).first() 
        return {
            'id': self.id,
            'category': {
                'category_id': self.category.id, 
                'category_name': self.category.name
            } if self.category else None,
            'farm': {
                'id': farm.id,
                'name' : farm.name,
                'address': farm.address,
                'city': farm.city,
                'state' : farm.state,
                'zipcode' : farm.zipcode,
                'link_url' : farm.link_url,
                'link_phone' : farm.link_phone,
            } if farm else None,
            'name' : self.name,
            'unit' : self.unit,
            'price': self.price,
            'count': self.count,
            'status': self.status,  # 0: active, 1: deleted
            'images': ast.literal_eval(self.images),
            'description' : self.description,
        }
    
    @staticmethod
    def get_by_id(id):
        if id is None or id == '':
            return None
        return Product.query.filter_by(id=id).first() 
    
    @staticmethod
    def get_by_farmid(farmid):
        if farmid is None or farmid == '':
            return None
        return Product.query.filter_by(farmid=farmid, status=0).all() 

    @staticmethod
    def get_all():
        return Product.query.filter_by(status=0).all()
    
    @staticmethod
    def getbyparam(ids, lower_price=0, upper_price=999999, keyword=''):
        if keyword=='':
            return Product.query.filter(Product.categoryid.in_(ids)).filter(Product.price.between(lower_price, upper_price)).filter_by(status=0).all()
        return Product.query.filter(Product.categoryid.in_(ids)).filter(Product.price.between(lower_price, upper_price)).\
            filter(Product.name.like('%'+keyword+'%')).filter_by(status=0).all()
        
    
    
class Basket(db.Model): # person cart 
    __tablename__ = 'basket'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    productid = db.Column('productid', db.Integer, db.ForeignKey('products.id'))
    productinfo  = db.relationship('Product', backref=backref('products', lazy=True, uselist=True))
    userid = db.Column('userid', db.Integer, nullable=False)
    # userinfo = db.relationship('User', backref=backref('users', lazy=True, uselist=True))
    buyunit   = db.Column(db.String(100)) # unit when create order
    buyprice  = db.Column(db.Float)       # price when create order
    count  =  db.Column(db.Integer)
    status = db.Column(db.Integer) # 0: not ordered, 1: ordered, 2: delivered
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __init__(self):
        self.buyunit  = ''
        self.buyprice = 0
        self.create_at = datetime.now()
        self.update_at = datetime.now()
    
    def to_dict(self):
        farm = None
        if (self.productinfo.farmid):
            farm = Farm.query.filter_by(id=self.productinfo.farmid).first() 
        return {
            'id'  : self.id,
            'userid': self.userid,
            'product': {
                'id': self.productinfo.id,
                'farmid': self.productinfo.farmid,
                'categoryid': self.productinfo.categoryid,
                'name' : self.productinfo.name,
                'price': self.productinfo.price,
                'count': self.productinfo.count,
                'unit' : self.productinfo.unit,
                'images': ast.literal_eval(self.productinfo.images),
                'description' : self.productinfo.description,
            },
            'farm': {
                'id': farm.id,
                'name' : farm.name,
                'address': farm.address,
                'city': farm.city,
                'state' : farm.state,
                'zipcode' : farm.zipcode,
                'link_url' : farm.link_url,
                'link_phone' : farm.link_phone,
            } if farm else None,
            'count': self.count,
            'buyunit': self.buyunit,
            'buyprice': self.buyprice,
            'status': self.status
        }

    @staticmethod
    def get_by_id(id):
        if id is None or id == '':
            return None
        return Basket.query.filter_by(id=id).first() 
    
    @staticmethod
    def get_by_productid(productid):
        if productid is None or productid == '':
            return None
        return Basket.query.filter_by(productid=productid).first()
    
    @staticmethod
    def get_by_id_status(productid, status):
        if productid is None or productid == '':
            return None
        return Basket.query.filter_by(productid=productid, status=status).first() 

    @staticmethod
    def get_by_ids(ids):
        if id is None or ids == '':
            return None
        return Basket.query.filter(Basket.id.in_(ids)).all() 

    @staticmethod
    def user_by_token(token):
        try:
            decoded_token = b64decode(bytearray(token, "ascii")).decode('utf-8')
            tokens = decoded_token.split(":")
            email = tokens[0]
            password = tokens[1]
            return User.query.filter_by(email=email, password=password).first()
        except:
            return None
    
    @staticmethod
    def get_by_userid(userid):
        if userid is None or userid == '':
            return None
        status = 0
        return Basket.query.filter_by(userid=userid, status=status).all() 
    
    @staticmethod
    def get_by_status(status):
        if status is None or status == '':
            return None
        return Basket.query.filter_by(status=status).all() 

    @staticmethod
    def get_all():
        return Basket.query.all()

class Card(db.Model): # person cart 
    __tablename__ = 'cards'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column('userid', db.Integer, nullable=False)
    branch = db.Column(db.String(256))
    number = db.Column(db.String(256))
    funding = db.Column(db.String(256))
    customerid = db.Column(db.String(256))
    
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __init__(self):
        self.create_at = datetime.now()
        self.update_at = datetime.now()
    
    def to_dict(self):
        return {
            'id'  : self.id,
            'userid': self.userid,
            'branch' : self.branch,
            'funding' : self.funding,
            'number': self.number,
            'customerid': self.customerid,
        }

    @staticmethod
    def get_by_id(id):
        if id is None or id == '':
            return None
        return Card.query.filter_by(id=id).first() 

    @staticmethod
    def card_by_token(token):
        try:
            decoded_token = b64decode(bytearray(token, "ascii")).decode('utf-8')
            tokens = decoded_token.split(":")
            email = tokens[0]
            password = tokens[1]
            user = User.query.filter_by(email=email, password=password).first()
            return Card.query.filter_by(userid=user.id).all()
        except:
            return None
    
    @staticmethod
    def get_by_userid(userid):
        if userid is None or userid == '':
            return None
        return Card.query.filter_by(userid=userid).all() 

    @staticmethod
    def get_all():
        return Card.query.all()

class Order(db.Model): # person order 
    __tablename__ = 'orders'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column('userid', db.Integer, nullable=False)
    farmid = db.Column('farmid', db.Integer, nullable=False)
    fname = db.Column(db.String(256))
    lname = db.Column(db.String(256))
    basketids = db.Column(db.String(5000))
    address  = db.Column(db.String(256))
    city     = db.Column(db.String(256))
    state    = db.Column(db.String(256))
    zipcode  = db.Column(db.String(100))
    email    = db.Column(db.String(256))
    phone    = db.Column(db.String(100))
    status   = db.Column(db.Integer)
    productcost = db.Column(db.Float)
    shipmentcost= db.Column(db.Float)
    paymentcost = db.Column(db.Float)
    
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __init__(self):
        self.create_at = datetime.now()
        self.update_at = datetime.now()
    
    def to_dict(self):
        farm = Farm.get_by_id(self.farmid)
        baskets = Basket.get_by_ids(ast.literal_eval(self.basketids))
        basketsinfo = []
        for basket in baskets:
            basketsinfo.append({
            'id'  : basket.id,
            'userid': basket.userid,
            'product': {
                'id': basket.productinfo.id,
                'farmid': basket.productinfo.farmid,
                'categoryid': basket.productinfo.categoryid,
                'name' : basket.productinfo.name,
                'price': basket.productinfo.price,
                'count': basket.productinfo.count,
                'unit' : basket.productinfo.unit,
                'images': ast.literal_eval(basket.productinfo.images),
                'description' : basket.productinfo.description,
            },
            'count': basket.count,
            'buyunit': basket.buyunit,
            'buyprice': basket.buyprice,
            'status': basket.status
            })
        return {
            'id'  : self.id,
            'userid': self.userid,
            'farmid': self.farmid,
            'fname': self.fname,
            'lname': self.lname,
            'basketids': ast.literal_eval(self.basketids),
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode' : self.zipcode,
            'email': self.email,
            'phone': self.phone,
            'productcost': self.productcost,
            'shipmentcost': self.shipmentcost,
            'paymentcost': self.paymentcost,
            'status': self.status,
            'created_at': str(self.create_at),
            'farm': {
                'id': farm.id,
                'name' : farm.name,
                'address': farm.address,
                'city': farm.city,
                'state' : farm.state,
                'zipcode' : farm.zipcode,
                'link_url' : farm.link_url,
                'link_phone' : farm.link_phone,
            } if farm else None,
            'basketsinfo': basketsinfo if basketsinfo else None
        }

    @staticmethod
    def get_by_id(id):
        if id is None or id == '':
            return None
        return Order.query.filter_by(id=id).first() 

    @staticmethod
    def order_by_token(token):
        try:
            decoded_token = b64decode(bytearray(token, "ascii")).decode('utf-8')
            tokens = decoded_token.split(":")
            email = tokens[0]
            password = tokens[1]
            user = User.query.filter_by(email=email, password=password).first()
            return Order.query.filter_by(userid=user.id).all()
        except:
            return None
    
    @staticmethod
    def get_by_userid(userid, offset, limit, keyword):
        if userid is None or userid == '':
            return None
        if keyword is None or keyword == '':
            return {
                'data': Order.query.filter_by(userid=userid).order_by(desc(Order.create_at)).offset(offset).limit(limit),
                'count': Order.query.filter_by(userid=userid).count()
            }
        return {
            'data': Order.query.filter_by(userid=userid).filter(Order.id.like('%'+keyword+'%')).order_by(desc(Order.create_at)).offset(offset).limit(limit),
            'count': Order.query.filter_by(userid=userid).filter(Order.id.like('%'+keyword+'%')).count()
        }


    @staticmethod
    def get_by_farmid(farmid, offset, limit, keyword):
        if farmid is None or farmid == '':
            return None
        if keyword is None or keyword == '':
            return {
                'data': Order.query.filter_by(farmid=farmid).order_by(desc(Order.create_at)).offset(offset).limit(limit),
                'count': Order.query.filter_by(farmid=farmid).count()
            }
        return {
            'data': Order.query.filter_by(farmid=farmid).filter(Order.id.like('%'+keyword+'%')).order_by(desc(Order.create_at)).offset(offset).limit(limit),
            'count': Order.query.filter_by(farmid=farmid).filter(Order.id.like('%'+keyword+'%')).count()
        }


    @staticmethod
    def get_all(offset, limit, key):
        return {
            'data': Order.query.order_by(desc(Order.create_at)).offset(offset).limit(limit),
            'count': Order.query.count()
        }
    
    @staticmethod
    def search(keyword=''):
        if keyword=='':
            return Order.query.all()
        return Order.query.filter(Order.id.like('%'+keyword+'%')).order_by(desc(Order.create_at)).all()

class Transaction(db.Model): # person transaction 
    __tablename__ = 'transactions'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column('userid', db.Integer, nullable=False)
    customerid = db.Column(db.String(256))
    customername = db.Column(db.String(5000))
    # orderid = db.Column('orderid', db.Integer, db.ForeignKey('orders.id'))
    # orderinfo  = db.relationship('Order', backref=backref('orders', lazy=True, uselist=True))
    orderid = db.Column('orderid', db.Integer, nullable=False)
    farmid = db.Column('farmid', db.Integer, nullable=False)
    farmname = db.Column(db.String(5000))
    basketids = db.Column(db.String(5000))
    amount  = db.Column(db.Float)
    currency = db.Column(db.String(256))
    status   = db.Column(db.Integer)
    
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __init__(self):
        self.create_at = datetime.now()
        self.update_at = datetime.now()
    
    def to_dict(self):
        return {
            'id'  : self.id,
            'userid': self.userid,
            'customerid': self.customerid,
            'customername': self.customername,
            'orderid': self.orderid,
            'farmid': self.farmid,
            'farmname': self.farmname,
            'basketids': ast.literal_eval(self.basketids),
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'date': str(self.create_at)
        }

    @staticmethod
    def get_by_id(id):
        if id is None or id == '':
            return None
        return Transaction.query.filter_by(id=id).first() 

    @staticmethod
    def transaction_by_token(token):
        try:
            decoded_token = b64decode(bytearray(token, "ascii")).decode('utf-8')
            tokens = decoded_token.split(":")
            email = tokens[0]
            password = tokens[1]
            user = User.query.filter_by(email=email, password=password).first()
            return Transaction.query.filter_by(userid=user.id).all()
        except:
            return None
    
    @staticmethod
    def get_by_userid(userid, offset, limit, keyword):
        if userid is None or userid == '':
            return None
        if keyword is None or keyword == '':
            return {
                'data': Transaction.query.filter_by(userid=userid).order_by(desc(Transaction.create_at)).offset(offset).limit(limit),
                'count': Transaction.query.filter_by(userid=userid).count()
            }
        return {
            'data': Transaction.query.filter_by(userid=userid).filter(Transaction.id.like('%'+keyword+'%')).order_by(desc(Transaction.create_at)).offset(offset).limit(limit),
            'count': Transaction.query.filter_by(userid=userid).filter(Transaction.id.like('%'+keyword+'%')).count()
        }

    @staticmethod
    def get_all(offset, limit, keyword):
        if keyword is None or keyword == '':
            return {
                'data': Transaction.query.order_by(desc(Transaction.create_at)).offset(offset).limit(limit),
                'count': Transaction.query.count()
            }
        return {
            'data': Transaction.query.filter(Transaction.customername.like('%'+keyword+'%')|Transaction.farmname.like('%'+keyword+'%')).order_by(desc(Transaction.create_at)).offset(offset).limit(limit),
            'count': Transaction.query.filter(Transaction.customername.like('%'+keyword+'%')|Transaction.farmname.like('%'+keyword+'%')).count()
        }
        


class Unit(db.Model): # product unit 
    __tablename__ = 'units'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name      = db.Column(db.String(256), nullable=False)
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __init__(self, name=''):
        self.name    = name
        self.create_at = datetime.now()
        self.update_at = datetime.now()
    
    def to_dict(self):
        return {
            'id'  : self.id,
            'name': self.name
        }

    @staticmethod
    def get_by_id(id):
        if id is None or id == '':
            return None
        return Unit.query.filter_by(id=id).first() 
    
    @staticmethod
    def find_by_name(name):
        if name is None or name == '':
            return False
        unit = Unit.query.filter_by(name=name).first()
        if unit is None:
            return False
        else:
            return True

    @staticmethod
    def get_all():
        return Unit.query.all()
