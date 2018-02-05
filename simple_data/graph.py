from collections import namedtuple

SINGULAR = 'singular'
PLURAL = 'plural'

BASIC_DOMAINS = {
     'numeric', 'int', 'text', 'datetime',
}

Edge = namedtuple('Edge', ('x', 'y',
                           'x_number',
                           'y_number',
                           'x_fieldname',
                           'y_fieldname' ))

def tuple_to_edge(t):
    x, y = t[:2]
    if len(t) == 2:
        numbers = PLURAL, SINGULAR
        names = y, x
    elif len(t) == 3:
        numbers = PLURAL, SINGULAR
        names = t[2], '%s_%s'%(t[2], x)
    elif len(t) == 4:
        numbers = t[2], t[3]
        names = y, x
    elif len(t) == 5:
        numbers = t[2], t[3]
        if numbers == (SINGULAR, PLURAL):
            x, y, = y, x
            numbers = numbers[::-1]
        names = t[4], '%s_%s' % (t[4], x)
    elif len(t) == 6:
        t = x, y, *numbers, *names
    # NB: has to be repeated since the first time it's been done to generate
    # a proper fieldname
    if numbers == (SINGULAR, PLURAL):
        x, y, = y, x
        numbers = numbers[::-1]
        names = names[::-1]
    t = x, y, *numbers, *names
    t = Edge(*t)
    return t


class Graph:
    def __init__(self, basic_domains=BASIC_DOMAINS):
        self.basic_domains = basic_domains
        self.nouns = set()
        self.edges = set()
        self.e = dict()

    def _add_edge(self, edge):
        if edge.x not in self.basic_domains:
            self.e[edge.x].add(edge)
        if edge.y not in self.basic_domains:
            self.e[edge.y].add(edge)
        self.edges.add(edge)

    def add_edges(self, edges):
        if not hasattr(edges, 'keys'):
            edges = [tuple_to_edge(t) for t in edges]
            for edge in edges:
                self._add_edge(edge)
        else:
            for edges in edges:
                for edge in edges:
                    edge = tuple_to_edge(edge)
                    self._add_edge(edge)
