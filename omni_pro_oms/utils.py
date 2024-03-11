from requests_oauthlib import OAuth1
import requests

def get_api(self, config, operation, body=None):
    headers = operation.headers
    
    request_params = {
        "method": operation.http_method,
        "url": config.base_url,
        "headers": headers
    }
    
    if config.auth == 'auth1':
        oauth = OAuth1(
            config.auth[config.auth]['consumer_key'],
            config.auth[config.auth]['consumer_secret'],
            config.auth[config.auth]['access_token'],
            config.auth[config.auth]['token_secret']
        )
        request_params['auth'] = oauth
    
    elif config.auth == 'auth2':
        headers['Authorization'] = config.auth[config.auth]['bearer_token'] + config.auth[config.auth]['token']
        
    if body:
        request_params['data'] = body
        
    response = requests.request(**request_params)
    
    return response
    
    