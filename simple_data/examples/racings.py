nouns = [
    # event is comprised of competitions
    # carried out in certain space-time region
    'event',
    # `competition` stands for a competition
    # between participants of the same `group`
    'competition',
    'lap', # `competition` may consist of several `lap`s
    'place',
    'person', # may include legal bodies
    'driver', # denotes driver's license
    'scrutineer', # scrutineer's license
    'automobile', # automobile's technical passport
    'scrutineering', # scrutineering certificate
    'classifiable', # discrete kinds; e.g. "homologation of harness" or seal
    'measurable', # measurable kinds; e.g. "fuel density" measured in "kg/m3"
]

edges = [
    # (X, Y)
    # (X, Y, X_fieldname)
    # (X, Y, X_number, Y_number)
    # (X, Y, 'singular', 'plural', Y_fieldname)
    # (X, Y, 'plural', 'singular', X_fieldname)
    # (X, Y, 'plural', 'plural', X_fieldname, Y_fieldname)
    #
    # each competition is a part of event
    ('event', 'competition', 'singular', 'plural'),
    # each lap is a part of competition
    ('competition', 'lap', 'singular', 'plural'),
    # each event is associated with a place
    ('event', 'place'),
    # a license is assocaited with a single person --- the owner
    ('driver', 'person')
    ('scrutineer', 'person')
    ('automobile', 'person', 'owner'),
    # issuer of the automobile passport
    ('automobile', 'scrutineer', 'issuer'),
    # the date a document was issued
    ('driver',     'datetime', 'issued'),
    ('scrutineer', 'datetime', 'issued'),
    ('automobile', 'datetime', 'issued'),
    # 
]

basicauth_nouns = [
    'person', 'user'
]

basicauth_edges = [

    ('user', 'person'),
    ('person', 'text', 'login')
    ('person', 'text', 'pwd')
]
