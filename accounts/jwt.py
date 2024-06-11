import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_jwt_token(name, email, id):
    expiration_time = datetime.now() + timedelta(hours=10)

    payload = {
        'user_id': id,
        'user': name,
        'email': email,
        'exp': expiration_time.timestamp(),  
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token


def decode_jwt_token(token):
    
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    return payload
    
