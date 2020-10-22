[mannual install environment]

# create virtual env
1. sudo apt install python3-venv
2. python -m venv venv
3. . venv/bin/activate 

# install flask package
4. pip install -r requirement.txt

# database migration & upgrade
5. python manage.py db init
6. python manage.py db migrate
7. python manage.py db upgrade
------------------------------
5.6.7. python create_db

# create admin
8. python manage.py create_admin

# run code
123. python manage.py runserver
 
