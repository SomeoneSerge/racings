from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL

from racings import domain


app = Eve(validator=ValidatorSQL, data=SQL)

db = app.data.driver
domain.Base.metadata.bind = db.engine
db.Model = domain.Base
db.create_all()

app.run(debug=True, use_reloader=False)
