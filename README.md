# udacity-book-catalog-final
Book catalog (CRUD app build with Python and SQLite+SQLAlchemy)

## Requirements

You will need Python and sqlite3 installed on your machine and accounts for
oauth providers you wish to use: Github, Google, Reddit.


## Installation and Running

1. Clone this project source code from Github:

        $ git clone https://github.com/JIghtuse/udacity-book-catalog-final.git
        $ cd udacity-book-catalog-final

2. Create API keys for oauth providers:

        https://developer.github.com/v3/oauth/
        https://developers.google.com/identity/protocols/OAuth2
        https://www.reddit.com/prefs/apps

3. Create secrets file with contents like:


        FLASH_SECRET = "<insert random long string here>"

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

4. Set desired port number in `main.py` (it should correspond to ports you
set when you created API keys).

5. Now you can launch project. It will be served at http://localhost:<port>

        $ python3 main.py

6. To deploy app, you will need to change callback URLs to your server address.


## Usage

Non-authorized users can only see books and categories (both in JSON and HTML).

Authorized users can create new books, edit and delete books.
