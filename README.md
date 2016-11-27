# udacity-book-catalog-final
Book catalog (CRUD app build with Python and SQLite+SQLAlchemy)

## Requirements

You will need Python and sqlite3 installed on your machine and accounts for
oauth providers you wish to use: Github, Google, Reddit.


## Installation and Running

1. Create project directory and launch installation script:

        $ sudo mkdir /var/www/catalog
        $ sudo chown $USER:$USER /var/www/catalog
        $ sh install.sh
        $ cd /var/www/catalog/

2. Create API keys for oauth providers:

        https://developer.github.com/v3/oauth/
        https://developers.google.com/identity/protocols/OAuth2
        https://www.reddit.com/prefs/apps

3. Create secrets.py file with contents like:


        FLASH_SECRET = "<insert random long string here>"
        DB_SECRET = "<insert database password here>"

        OAUTH_PROVIDER_SECRETS = {
            'reddit': {
                'client_id': "<your reddit client id>",
                'client_secret': "<your reddit client secret>",
            },
            'github': {
                'client_id': "<your github client id>",
                'client_secret': "<your github client secret>",
            },
            'google': {
                'client_id': "<your google client id>",
                'client_secret': "<your google client secret>",
            }
        }


4. Modify oauth.py file lines with `redirect_uri` to match your server IP
address, e.g:

        # ...
        'google': {
            # ...
            'redirect_uri': "http://192.0.2.1/callback/google",
            # ...
        }
        # ...

5. Create PostgreSQL database and user for application:

        postgres=# create user catalog with password '<database password>';
        postgres=# alter role catalog with login;
        postgres=# alter role catalog createdb ;
        postgres=# create database catalog with owner catalog;
        postgres=# \c catalog
        catalog=# revoke all on SCHEMA public from public;
        catalog=# grant all on SCHEMA public to catalog;

6. To run locally, user main.py script:

        python3 main.py

7. To run with apache, allow server to proxy connections to 5000 port:

        <Location />
                ProxyPass http://localhost:5000
                ProxyPassReverse http://localhost:5000
        </Location>

## Usage

Non-authenticated users can only see books and categories (both in JSON and HTML).

Authenticated and authorized users can create new books, edit and delete their books.


## Running instance

There is a running instance of an app at the url http://35.160.212.183/

NOTE: Google currently forbids using IP address for callback URL, so
authorization with Google does not work on this machine.
