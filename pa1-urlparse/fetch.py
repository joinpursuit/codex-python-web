#
# Assignment: Write a function to parse URLs.
# 
# Fill in the body of the 'urlparse()' function in this module.  If you wish,
# you may define and use additional helper functions; these generally will make
# your code clearer.
#
# To test your solution, use the unit test script provided along with this file.
# The unit test script will import your version of this module, and test your
# solution by running it with specific inputs and checking the answers.  It will
# tell you if all the tests produce the expected results or not.
#

from collections import namedtuple
from urllib import request

ParseResult = namedtuple('ParseResult', 'scheme, netloc, path, params, query, fragment')


def urlparse(url):
    '''
    Parses a URL and returns a 'ParseResult' of its components.

    Below is an example URL with its components listed by name:

       foo://example.com:8042/over/there?name=ferret#nose
       \_/   \______________/\_________/ \_________/ \__/
        |           |            |            |        |
       scheme     authority     path        query   fragment

    For details, see: http://tools.ietf.org/html/rfc3986#section-3.1

    For example,

      >>> urlparse('foo://example.com:8042/over/there?name=ferret#nose')
      ParseResult(scheme='foo', netloc='example.com:8042', path='/over/there', params='', query='name=ferret', fragment='nose')

    '''
    scheme = netloc = path = params = query = fragment = ''

    return ParseResult(scheme, netloc, path, params, query, fragment)
