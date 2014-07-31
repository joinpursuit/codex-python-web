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
    # Split the text into paragraphs.
    pars = split_paragraphs(text)
    for par in pars:
        # Split the paragraph into words by separating at each space.
        words = split(par, ' ')
        # Keep track of the length of the line we've printed so far.
        length = 0
        for word in words:
            # Include a space after each word.
            word += ' '
            # If we printed this word, how long would the line be?
            if length + len(word) > width:
                # The line would be too long.  End this line.
                # Now print the word on the next line.
                print()
                length = 0
            print(word, end='')
            length += len(word)
        # End of the paragraph: end the current line in progress.
        print()
        # Leave a blank line.
        print()
        
        
