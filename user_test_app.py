#!/usr/bin/python3

from flask_security import current_user, auth_required, hash_password
from flask import render_template_string
from is_logged_in import is_logged_in
from werkzeug.test import Client
from logging_hooks import *
from database import db
from app import app
import os

def run_tests(app):
    
    app.config['WTF_CSRF_ENABLED'] = False
    
    test_client=login_test_client()
    
    mal=assure_mal_not_logged_in()
    
def assure_mal_not_logged_in():
    mal_client=Client(app)
    
    response=mal_client.get('/is_logged_in')
    assert response.status_code == 200
    
    assert response.json==False
    
    return mal_client

    
def login_test_client():
    test_client=Client(app)
    
    result=test_client.post('/login', json={
        'next': '/', 
        'email': 'test@me.com',
        'password' : 'password',
        'remember': 'y', 
        'submit': 'Login',
    })
    assert result.status_code == 200
    
    response=test_client.get('/is_logged_in')
    assert response.status_code == 200
    
    assert response.json==True
    
    return test_client

if __name__ == '__main__':
    with app.app_context():
        import models
        db.create_all()
        # Create a user to test with
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(email="test@me.com", password=hash_password("password"))
        db.session.commit()
        
        run_tests(app)
        
        #app.run(host='0.0.0.0', port=9000)
    
    
