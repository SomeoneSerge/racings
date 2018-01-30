from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from eve.auth import TokenAuth as _TokenAuth
import json
import base64

from flask import request, jsonify
from werkzeug.exceptions import Unauthorized
from racings.domain import User
from racings import domain


class TokenAuth(_TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        login = domain.User.verify_auth_token(token)
        if login and allowed_roles:
            user = app.data.driver.session.query(domain.User).get(login)
            return user.isAuthorized(allowed_roles)
        else:
            return False



def register_views(app):

    @app.route('/login', methods=['POST'])
    def login(**kwargs):
        """Simple login view that expect to have username
        and pw in the request POST. If the username and
        pw matches - token is being generated and return.
        """
        data = request.get_json()
        login = data.get('username')
        pw = data.get('pw')

        if not login or not pw:
            raise Unauthorized('Provide username and pw.')
        else:
            user = app.data.driver.session.query(User).get(login)
            if user and user.check_pw(pw):
                token = user.generate_auth_token()
                return jsonify({'token': token.decode('ascii')})
        raise Unauthorized('Wrong username and/or pw.')

app = Eve(validator=ValidatorSQL, data=SQL)
register_views(app)

db = app.data.driver
domain.Base.metadata.bind = db.engine
db.Model = domain.Base
db.create_all()

app.run(debug=True, use_reloader=False)
