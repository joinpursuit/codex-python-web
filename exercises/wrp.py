def split(text, sep):
    '''
    Divides up some a string 'text' at each occurrence of a separator 'sep'.

    Returns a list of parts of the text, with the separators removed.
    '''
    # Start with an empty list of parts.
    parts = []
    while True:
        # Find the next occurrence of the separator.
        idx = text.find(sep)
        if idx == -1:
            # No more.  Add the rest of the text.
            parts.append(text)
            # And we're done.
            return parts
        else:
            # Found a separator.  Take the text up to it.
            part = text[: idx]
            parts.append(part)
            # And skip over it.
            text = text[idx + len(sep) :]


def split_paragraphs(text):
    '''
    Splits text into a list of paragraphs.
    '''
    # Start a list of paragraphs, initially empty.
    pars = []
    # Start off the first paragraph, initially empty.
    this_par = ''
    # Split the text into lines.
    lines = split(text, '\n')
    # Now process each line.
    for line in lines:
        if len(line) > 0:
            # Add this to the current paragraph.
            if len(this_par) > 0:
                this_par += ' '
            this_par += line
        else:
            # Blank line: that's the end of the paragraph (unless it's empty).
            if len(this_par) > 0:
                # Store this paragraph.
                pars.append(this_par)
                # Start a new paragraph.
                this_par = ''
    # Make sure we add the last paragraph.
    if len(this_par) > 0:
        pars.append(this_par)

    return pars


def print_wrapped(text, width):
    '''
    Prints text, wrapped to a maximum line width.
    '''
    # FIXME: Write me!
    #
    # Notes:
    #
    # - To print some text and end the line:
    #     print(text)
    # - To print some text without ending the line:
    #     print(text, end='')
    # - To end the current line, or leave a blank line:
    #     print()
    #
    # You will have to keep track of the length of the current line.


