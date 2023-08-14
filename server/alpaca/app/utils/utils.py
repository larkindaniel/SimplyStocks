import cognitojwt

class CognitoResponse(object):
    def __init__(self, access_token, refresh_token, cognito_user_id=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.cognito_user_id = cognito_user_id