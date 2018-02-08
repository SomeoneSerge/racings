from bson.objectid import ObjectId
from datetime import datetime
from pyrsistent import m, s, v
from racings.tools import pyrsistent_to_mutable

SAMPLE_DATA = m(
    players=v(
        m(_id=ObjectId(),
          firstname='Serge',
          lastname='K',
          phone='1000000000',
          email='newkozlukov@gmail.com',
          address='Nonexistence'),
        m(_id=ObjectId(),
          firstname='Julia',
          lastname='L',
          phone='1000000001',
          email='jlev@racings.ru'),
        m(_id=ObjectId(),
          firstname='FIA',
          phone='+44 (0)20 7929 0081',
          email='info@fia.org')))
SAMPLE_DATA += m(
    scrutineers=v(
        m(doc_no='1',
          holder=m(
              name='Julia Levitskaya',
              id=SAMPLE_DATA['players'][1]['_id'],
              collection='players'),
          issuer=m(
              name='FIA',
              id=SAMPLE_DATA['players'][2]['_id'],
              collection='players'),
          valid_thru=datetime(datetime.now().year + 3, 1, 1))))

SAMPLE_DATA = pyrsistent_to_mutable(SAMPLE_DATA)
