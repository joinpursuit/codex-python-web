def parse_csv(text):
    '''
    Parses CSV with a header.  Returns a list of dicts, one per line of data.
    '''
    # Split the text into lines.
    lines = text.split('\n')
    # The header is the first line; remaining lines contain data.
    header = lines[0]
    data_lines = lines[1 :]
    # The columns names are in the header.
    names = header.split(',')
    # Start with empty data.
    data = []
    for line in data_lines:
        # Split the line into individual values.
        values = line.split(',')
        # Pair up the names and values, and store them in a row.
        row = {}
        for name, value in zip(names, values):
            row[name] = value
        # Store the row.
        data.append(row)
    return data

    
