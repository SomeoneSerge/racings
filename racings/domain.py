from datetime import date
from pyrsistent import m, s  # immutable dict (map) and set

# Cerberus schema


def t(type, **kwargs):
    return m(type=type) + kwargs


_T_NAME = m(
    type='string',
    minlength=1,
    maxlength=512,
)

_T_REF = m(name=_T_NAME, ref=t('dbref'))
_T_PAST_DATE = m(type='integer', min=1800, max=date.today().year)

# Fancy-named legal bodies.
# Includes persons and organizations.
PLAYERS = m(
    firstname=_T_NAME,
    lastname=_T_NAME,
    address=t('string'),
    email=t('string', minlength=5, maxlength=512),
    phone=t('string', maxlength=15))

DOCUMENT_BASE = m(
    doc_no=t('string', minlength=2, maxlength=128, unique=True),
    issued=_T_PAST_DATE,
    valid_thru=t('datetime'),
    issuer=_T_REF,
)

LICENSE_BASE = DOCUMENT_BASE + m(holder=_T_REF)

# Scrutineer's license
SCRUTINEERS = LICENSE_BASE
# Driver's license
DRIVERS = LICENSE_BASE

AUTOMOBILE_BASE = m(
    doc_no=DOCUMENT_BASE['doc_no'],
    holder=LICENSE_BASE['holder'],
    model=t('string'),
    groups=m(type='list', schema=_T_REF),
    homologation=t('dbref'),
    homologation_no=t('string'),
)

# Automobile passport
AUTOMOBILES = LICENSE_BASE + AUTOMOBILE_BASE + m(
    chassis=m(type='string'),
    engine=m(type='string'),
    engine_year=_T_PAST_DATE,
    make=t('string'),
    cubcap_nominal=t('integer'),
    cubcap_derived=t('integer'),
    wheeldrive=t('string', allowed=s('forward', 'rear', 'full')),
    previous_passport=t('dbref'),
    modifications=t(
        'list',
        schema=t(
            'dict',
            schema=m(
                description=t('string'), scrutineer=_T_REF,
                date=_T_PAST_DATE))))
HOMOLOGATIONS = DOCUMENT_BASE
SEAL_BASE = m(
    doc_no=DOCUMENT_BASE['doc_no'],
    kind=t('string'),
    detail=t('string'),
)
SEALS = DOCUMENT_BASE + SEAL_BASE + m(broken=t('boolean'))
SCRUTINEERINGS = DOCUMENT_BASE + m(
    competition=_T_REF,
    group=t('string'),
    starting_no=t('integer'),
    team=t('string'),
    automobile=t(
        'dict',
        schema=AUTOMOBILE_BASE +
        m(driver=_T_REF,
          seals=t(
              'list', schema=t('dict',
                               schema=m(ref=t('dbref')) + SEAL_BASE)))),
    new_seals=t(
        'list', schema=t('dict', schema=SEAL_BASE + m(ref=t('dbref')))),
    notes=t('list', schema=t('string')),
)

DOMAIN = m(
    players=m(item_name='person', schema=PLAYERS),
    scrutineers=m(item_name='scrutineer', schema=SCRUTINEERS),
    drivers=m(item_name='driver', schema=DRIVERS),
    automobiles=m(item_name='automobile', schema=AUTOMOBILES),
    homologations=m(item_name='homologation', schema=HOMOLOGATIONS),
    seals=m(item_name='seal', schema=SEALS),
)
