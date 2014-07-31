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


