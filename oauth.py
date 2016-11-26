from secrets import OAUTH_PROVIDER_SECRETS

OAUTH_PROVIDER_DATA = {
    'reddit': {
        'auth_url': "https://ssl.reddit.com/api/v1/authorize?",
        'access_token_url': "https://ssl.reddit.com/api/v1/access_token",
        'oauth_url': "https://oauth.reddit.com/api/v1/",
        'redirect_uri': "http://localhost:8888/callback/reddit",
        'revoke_url': "https://www.reddit.com/api/v1/revoke_token",
        'client_id': OAUTH_PROVIDER_SECRETS['reddit']['client_id'],
        'client_secret': OAUTH_PROVIDER_SECRETS['reddit']['client_secret'],
        'revoke_method': 'POST',
        'user_request': 'me',
        'user_name_field': 'name',
        'auth_header_name': 'bearer',
        'scope': "identity",
    },
    'github': {
        'auth_url': "https://github.com/login/oauth/authorize?",
        'access_token_url': "https://github.com/login/oauth/access_token",
        'oauth_url': "https://api.github.com/",
        'redirect_uri': "http://localhost:8888/callback/github",
        # TODO: find revoke for github
        'revoke_url': "",
        'revoke_method': 'NONE',
        'client_id': OAUTH_PROVIDER_SECRETS['github']['client_id'],
        'client_secret': OAUTH_PROVIDER_SECRETS['github']['client_secret'],
        'user_request': 'user',
        'user_name_field': 'name',
        'auth_header_name': 'token',
        'scope': "identity",
    },
    'google': {
        'auth_url': "https://accounts.google.com/o/oauth2/auth?",
        'access_token_url': "https://accounts.google.com/o/oauth2/token",
        'redirect_uri': "http://localhost:8888/callback/google",
        'oauth_url': "https://www.googleapis.com/oauth2/v1/",
        'revoke_url': "https://accounts.google.com/o/oauth2/revoke?",
        'client_id': OAUTH_PROVIDER_SECRETS['google']['client_id'],
        'client_secret': OAUTH_PROVIDER_SECRETS['google']['client_secret'],
        'revoke_method': 'GET',
        'user_request': 'userinfo',
        'user_name_field': 'name',
        'auth_header_name': "OAuth",
        'scope': "https://www.googleapis.com/auth/userinfo.email",
    }
}
