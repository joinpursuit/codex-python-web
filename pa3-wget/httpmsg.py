"""
HTTP version 1.1 partial protocol implementation.

See RFC2616 for the protocol specification:
  http://www.w3.org/Protocols/rfc2616/rfc2616.html

NOTE: This module is for illustration purposes only, and does not implement the
complete, correct protocol.  Do not use in production code.
"""

#-------------------------------------------------------------------------------
# Imports

import collections

#-------------------------------------------------------------------------------
# Constants
# 
# These are fixed values used throughout the module.  By convention, we use
# names in ALL_CAPITALS to indicate constants.

# The protocol version implemented in this module.
HTTP_VERSION = 'HTTP/1.1'

# Headers must be encoded with ISO-8859-1 (aka "Latin-1").
HEADER_ENCODING = 'iso-8859-1'

# The end-of-line (EOL) sequence.
EOL = '\r\n'

# For clarity below, we assign names to these single characters.
SPACE = ' '
COLON = ':'

#-------------------------------------------------------------------------------
# Types

# An HTTP request.
Request = collections.namedtuple(
    'Request',
    ('method',  # (str) The request method.
     'path',    # (str) The path to the requested page.
     'header',  # (dict) Dict of field names to field values.
     'body',    # (bytes) Body data.
    ))

# An HTTP response.
Response = collections.namedtuple(
    'Response',
    ('status',  # (int) The status code.
     'reason',  # (str) Description of the reason for the status code.
     'header',  # (dict) Dict of field names to field values.
     'body',    # (bytes) Body data.
    ))

#-------------------------------------------------------------------------------
# Helper functions
#
# These functions are intended for use only in implementing other functions in
# this module, rather than by other people.  They are called "helper functions"
# and in Python by convention are given names starting with an underscore.

def _split_lines(msg):
    """
    Splits a protocol message into lines until the first blank line.

    'msg' is a byte array containing a protocol message.  Divides up the message
    into lines, until it finds a blank line.  These lines have the EOL
    characters removed, and are decoded to strings.  Returns a list of lines,
    and a byte array of the remainder of the message.
    """
    # Find the EOL sequence encoded as bytes.
    eol = EOL.encode(HEADER_ENCODING)

    # The list into which we will collect header lines.
    lines = []
    # Keep going until we find a blank line.
    while True:
        # Look for the EOL sequence.
        index = msg.index(eol)
        # Split off the line, not including the EOL.
        line = msg[: index]
        # In the message, skip over the line, past the EOL.
        msg = msg[index + len(eol) :]
        # Is the line blank?
        if len(line) == 0:
            # Yes.  We're done; return the lines and whatever data is left in
            # the message.
            return lines, msg
        else:
            # No.  Decode the line.
            line = line.decode(HEADER_ENCODING)
            # Store it in the list of lines.
            lines.append(line)
            # Now continue at the top of the loop.


def _format_header(fields):
    """
    Formats a header from fields.

    'fields' is a dict from field names to values.  Returns a list of header
    lines.
    """
    # The list into which we will collect header lines.
    lines = []
    for name, value in fields.items():
        # A header line looks like, "name: value".
        line = name + COLON + SPACE + value
        # Add this line to the list.
        lines.append(line)
    return lines


def _parse_header(lines):
    """
    Parses lines from a header.

    'lines' is a list of strings of header lines.  Parses these into name-value
    pairs, and return a dict from name to value.
    """
    # The dict into which we will store header fields.
    header = {}
    # Loop over lines in the header.
    for line in lines:
        # Find the first colon.
        index = line.index(COLON)
        # Up to the colon is the field name.
        name = line[: index]
        # After the colon is the field value.
        value = line[index + 1 :]
        # The field value may begin or end with extra space, which is not 
        # significant.  Remove it.
        value = value.strip()
        # Store the field.
        header[name] = value
    # All done.
    return header


def _format_message(start_line, header, body):
    """
    Formats an HTTP protocol message from a start line, header, and body.

    'start_line' is the start line string; 'header' is a dict from field name
    to value; 'body' is a byte array of the message body.  Returns the message
    as a byte array.
    """
    # The message begins with the start line, terminated with EOL and encoded.
    msg = (start_line + EOL).encode(HEADER_ENCODING)
    # Convert the header to lines.
    header_lines = _format_header(header)
    # Add them to the message, one by one, each terminated with EOL and encoded.
    for line in header_lines:
        msg = msg + (line + EOL).encode(HEADER_ENCODING)
    # A blank line indicates end of headers.
    msg = msg + EOL.encode(HEADER_ENCODING)
    # The rest of the message is the body.
    msg = msg + body
    return msg


def _parse_message(msg):
    """
    Divides an HTTP protocol message into start line, header, and body.

    'msg' is a byte array containing the message.  Returns the start line, with
    the EOL marker removed and decoded into a string; the header, as a dict from
    field name to field value; and the body as a byte array.
    """
    lines, body = _split_lines(msg)
    # The first line is the start line.
    start_line = lines[0]
    # Remaining lines are the header.
    header = _parse_header(lines[1 :])
    return start_line, header, body
    

def _format_request_line(method, path):
    """
    Formats the request line.

    'method' is the request method; 'path' is the requested path.  Returns
    the request line as a str.
    """
    return method + SPACE + path + SPACE + HTTP_VERSION


def _parse_request_line(line):
    """
    Parses the request line.

    Returns the method and path.
    """
    # Up to the first space is the method.
    index0 = line.index(SPACE)
    method = line[: index0]
    # Starting from the first space, up to the next space is the path.
    index1 = line.index(SPACE, index0 + 1)
    path = line[index0 + 1 : index1]
    # The remainder is the protocol version.
    http_version = line[index1 + 1 :]
    # Make sure it's the protocol version we recognize.
    assert http_version == HTTP_VERSION
    return method, path


def _format_status_line(status, reason):
    """
    Formats the status line.

    'status' is the status code as an integer.  Returns the status line as a 
    str.
    """
    return HTTP_VERSION + SPACE + str(status) + SPACE + reason


def _parse_status_line(line):
    """
    Parses the status line.

    Returns the status code and reason.
    """
    # Up to the first space is the protocol version.
    index0 = line.index(SPACE)
    http_version = line[: index0]
    # Make sure it's the protocol version we recognize.
    assert http_version == HTTP_VERSION
    # Starting from the first space, up to the next space is the status code.
    index1 = line.index(SPACE, index0 + 1)
    status = line[index0 + 1 : index1]
    # Convert the status code to an integer.
    status = int(status)
    # The remainder is the reason.
    reason = line[index1 + 1 :]
    return status, reason


def format_request(request):
    """
    Formats a request into a protocol message.

    'request' is a 'Request' object.  Returns a byte array.
    """
    start_line = _format_request_line(request.method, request.path)
    msg = _format_message(start_line, request.header, request.body)
    return msg


def parse_request(msg):
    """
    Parses a request protocol message.

    'msg' is a byte array containing the request message.  Returns a 'Request'
    object.
    """
    start_line, header, body = _parse_message(msg)
    request, path = _parse_request_line(start_line)
    return Request(request, path, header, body)


def format_response(response):
    """
    Formats a response into a protocol message.

    'response' is a 'Response' object.  Returns a byte array.
    """
    start_line = _format_status_line(response.status, response.reason)
    msg = _format_message(start_line, response.header, response.body)
    return msg


def parse_response(msg):
    """
    Parses a response message.

    'msg' is a byte array containing the response message.  Returns a 'Response'
    object.
    """
    start_line, header, body = _parse_message(msg)
    status, reason = _parse_status_line(start_line)
    return Response(status, reason, header, body)


