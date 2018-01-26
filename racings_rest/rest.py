from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from eve.auth import TokenAuth as _TokenAuth

from racings import domain


class TokenAuth(_TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        login = domain.User.verify_auth_token(token)
        if login and allowed_roles:
            user = app.data.driver.session.query(domain.User).get(login)
            return user.isAuthorized(allowed_roles)
        else:
            return False


app = Eve(validator=ValidatorSQL, data=SQL)

db = app.data.driver
domain.Base.metadata.bind = db.engine
db.Model = domain.Base
db.create_all()

app.run(debug=True, use_reloader=False)
