from secrets import OAUTH_PROVIDER_SECRETS

OAUTH_PROVIDER_DATA = {
    'reddit': {
        'auth_url': "https://ssl.reddit.com/api/v1/authorize?",
        'access_token_url': "https://ssl.reddit.com/api/v1/access_token",
        'oauth_url': "https://oauth.reddit.com/api/v1/",
        'redirect_uri': "http://localhost:65010/reddit_callback",
        'client_id': OAUTH_PROVIDER_SECRETS['reddit']['client_id'],
        'client_secret': OAUTH_PROVIDER_SECRETS['reddit']['client_secret'],
    },
    'github': {
        'auth_url': "https://github.com/login/oauth/authorize?",
        'access_token_url': "https://github.com/login/oauth/access_token",
        'oauth_url': "https://api.github.com/",
        'redirect_uri': "http://localhost:65010/github_callback",
        'client_id': OAUTH_PROVIDER_SECRETS['github']['client_id'],
        'client_secret': OAUTH_PROVIDER_SECRETS['github']['client_secret'],
    },
    'google': {
        'auth_url': "https://accounts.google.com/o/oauth2/auth",
        'access_token_uri': "https://accounts.google.com/o/oauth2/token",
        'redirect_uri': "http://localhost:65010/googleplus_callback",
        'oauth_url': "https://www.googleapis.com/oauth2/v1/",
        'client_id': OAUTH_PROVIDER_SECRETS['google']['client_id'],
        'client_secret': OAUTH_PROVIDER_SECRETS['google']['client_secret'],
    }
}
