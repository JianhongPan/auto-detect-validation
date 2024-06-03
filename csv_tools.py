import os
import csv
from datetime import datetime

from attr import fields

def save_to_csv(save_path:str, fields:list, rows:list):
    ''' 
    Save the results to a csv file
    '''
    if not os.path.exists(save_path):
        with open(save_path, 'w') as f:
            pass
    
    import csv
    with open(save_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)

    with open(save_path, 'a') as f:
        writer = csv.writer(f)
        # if the first line is not the header, write the header
        if not header:
            writer.writerow(fields)
        # check if the each field in the header
        elif any(field not in fields for field in header):
            raise ValueError("The header of the csv file is not correct.")
        
        # resort the fields in the rows according to the header
        rows = [[row[fields.index(field)] for field in header] for row in rows]
        writer.writerows(rows)

def read_from_csv(read_path:str):
    ''' 
    Read a csv file
    '''
    with open(read_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            return list()
        rows = list()
        for row in reader:
            rows.append(row)
    return header, rows

def fields_select(csv, fields:list):
    '''
    Filter the fields based on the fileds
    '''
    header, rows = csv
    rows = [[row[header.index(field)] for field in fields] for row in rows]
    return fields, rows

def get_mapping(mapping_csv):
    '''
    Get the mapping function according to the csv file, e.g.,
    `get_mapping(mapping_csv)`, where `mapping_csv`: the csv file that contains the mapping, e.g., \\
    `from,to`   \\
    `0.82,82`   \\
    `0.31,31`   \\.

    The mapping function can be used to map the value to the corresponding value, e.g.,
    `mapping(0.82) -> 82`.
    '''
    header, rows = mapping_csv
    from_idx, to_idx = header.index('from'), header.index('to')
    mapping_dict = {row[from_idx]: row[to_idx] for row in rows}
    def mapping(x):
        return mapping_dict[x] if x in mapping_dict else x
    return mapping

def field_apply(csv, field:list, func):
    '''
    Apply the function to the fields
    '''
    header, rows = csv
    field_index = header.index(field)
    rows = [[func(item) if i == field_index else item for i, item in enumerate(row)] for row in rows]
    return header, rows

def rows_filter(rows:list, *regexes):
    '''
    Filter the rows based on the regexes
    '''
    rows = [row for row in rows if all(regex in row for regex in regexes)]
    return rows


def rows_to_2dcoordinates(rows):
    '''
    Convert the rows to coordinates
    '''
    x, y = dict(), dict()
    for row in rows:
        x[row[0]] = 0
        y[row[1]] = 0
    x = [key for key in x]
    y = [key for key in y]

    z = [[0 for _ in range(len(y))] for _ in range(len(x))]

    for row in rows:
        x_index, y_index = x.index(row[0]), y.index(row[1])
        z[x_index][y_index] = row[2]

    return x, y, z

def get_current_time():
    ''' 
    Get the current time
    '''
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")