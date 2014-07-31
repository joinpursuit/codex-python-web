from collections import namedtuple
from urllib import request

Parts = namedtuple(
    'Parts', 
    ['scheme', 
     'authority', 
     'full_path',  # Everything following the authority.
     'path', 
     'params', 
     'query', 
     'fragment'])


def parse(url):
    '''
    Parses a URL and returns a 'Parts' of its components.

    Below is an example URL with its components listed by name:

       foo://example.com:8042/over/there?name=ferret#nose
       \_/   \______________/\_________/ \_________/ \__/
        |           |            |            |        |
       scheme     authority     path        query   fragment

    For details, see: http://tools.ietf.org/html/rfc3986

    For example,

      >>> urlparse('foo://example.com:8042/over/there?name=ferret#nose')
      Parts(scheme='foo', authority='example.com:8042', full_path='/over/there?name=ferret#nose', path='/over/there', params='', query='name=ferret', fragment='nose')

    '''
    scheme = authority = full_path = path = params = query = fragment = ''

    # Handle scheme
    i = url.find(':')
    if i > 0:
        url, scheme = _parse_scheme(url, i)

    # Handle authority / authority / domain
    if url[:2] == '//':
        url, authority = _parse_authority(url)

    # Everything after the authority is the full path.
    full_path = url

    # Handle path
    url, path = _parse_path(url)
  
    # Handle query string and fragment
    if len(url) > 0 and url[0] == '?':
        query, fragment = _parse_query(url)

    return Parts(scheme, authority, full_path, path, params, query, fragment)


def _parse_scheme(url, i):
    '''
    "Scheme names consist of a sequence of characters beginning with a letter
    and followed by any combination of letters, digits, plus ("+"), period
    ("."), or hyphen ("-")."
    Check for port
    '''
    if url[i+1].isdigit():
        scheme = ''
    else:
        scheme = url[:i].lower()
        url = url[i+1:]
    return url, scheme


def _parse_authority(url):
    '''
    "The authority component is preceded by a double slash ("//") and is
    terminated by the next slash ("/"), question mark ("?"), or number sign
    ("#") character, or by the end of the URI.
    '''
    url = url[2:]
    minI = None
    for c in '/?#':
        i = url.find(c)
        if i > 0 and (minI == None or i < minI):
            minI = i
    if minI != None:
        authority = url[:minI]
        url = url[minI:]
    else:
        authority = url
        url = ''
    return url, authority


def _parse_path(url):
    '''
    "The path is terminated by the first question mark ("?") or number sign
    ("#") character, or by the end of the URI."
    '''
    minI = None
    for c in '?#':
        i = url.find(c, 1)
        if i > 0 and (minI == None or i < minI):
            minI = i
    if minI != None:
        path = url[:minI]
        url = url[minI:]
    else:
        path = url
        url = ''
    return url, path


def _parse_query(url):
    '''
    "The query component is indicated by the first question mark ("?")
    character and terminated by a number sign ("#") character or by the end
    of the URI."

    "A fragment identifier component is indicated by the presence of a number
    sign ("#") character and terminated by the end of the URI."
    '''
    # +1 to remove "?"
    query = url[1:]
    j = query.find('#', 1)
    if j > 1:
        # +1 to remove "#"
        fragment = query[j+1:]
        query = query[:j]
    else:
        fragment = ''
    return query, fragment


