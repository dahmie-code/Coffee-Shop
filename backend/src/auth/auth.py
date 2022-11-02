import json
from lib2to3.pgen2 import token
from os import abort
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'funp.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee-shop-app'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
Implement get_token_auth_header() method
'''   
"""Obtains the access token from the Authorization header"""
def get_token_auth_header():
   auth = request.headers.get('Authorization', None)
   if not auth:
       raise AuthError({
           'code': 'authorization_header_missing',
           'description': 'Authorization header is expected.'
       }, 401)
       
    # split bearer and the token   
   separates = auth.split()
   
   #    raises AuthErrors if the header is malformed
   if separates[0].lower() != 'bearer':
           raise AuthError({
           'code': 'invalid_header',
           'description': 'Authorization header must start with "Bearer".'
       }, 401)
       
   elif len(separates) == 1:
       raise AuthError({
           'code': 'invalid_header',
           'description': 'Token not found.'
       }, 401)
       
   elif len(separates) > 2:
       raise AuthError({
           'code': 'invalid_header',
           'description': 'Authorization header must be bearer token.'
       }, 401)
       
   token = separates[1]
    # return the token part of the header
   return token

'''
Implement check_permissions(permission, payload) method
'''
"""User permission verification"""
def check_permissions(permission, payload):
    # raise an AuthError if permissions are not included in the payload
    if 'permissions' not in payload:

        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permission not included in JWT.'
        }, 400)
        
    # raise an AuthError if the requested permission string is not in the payload permissions array.        
    if permission not in payload['permissions']:

        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)   
    # return true otherwise
    return True

'''
Implement verify_decode_jwt(token) method
'''
def verify_decode_jwt(token):
    """Validates Auth0 JWTs"""
# token: a json web token (string)
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.wellknown/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key ={}
    
    # an Auth0 token with key id (kid)
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization invalid.'
        }, 401)
    # verify the token using Auth0 /.well-known/jwks.json
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n'  : key['n'],
                'e'  : key['e']
            }
    # decode the payload from the token
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/' 
            )
            
            # return the decoded payload
            return payload
        
        # validate the claims
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Expired Token'
            }, 401)
            
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Kindly, check the issuer and the audience.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authentication token not parsed.'
            }, 400)
        
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Appropriate key not found'
    }, 400)
'''
Implement @requires_auth(permission) decorator method 
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # the get_token_auth_header method to get the token
            token = get_token_auth_header()
            try:
                # the verify_decode_jwt method to decode the jwt
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            # the check_permissions method validate claims and check the requested permission
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    # return decorator which passes the decoded payload to the decorated method
    return requires_auth_decorator