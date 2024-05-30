import os

def save_to_csv(save_path:str, **row):
    ''' 
    Save the results to a csv file
    '''
    if not os.path.exists(save_path):
        with open(save_path, 'w') as f:
            pass
    
    import csv
    with open('results.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)

    with open('results.csv', 'a') as f:
        writer = csv.writer(f)
        # if the first line is not the header, write the header
        if not header:
            writer.writerow([*row.keys()])
        # check if the fields in the header exist in the row
        elif all(key in header for key in row.keys()):
            raise ValueError("The header of the csv file is not correct.")
        
        # resort the fields in the row according to the header
        row = {key: row[key] for key in header}
        writer.writerow([*row.values()])

def read_from_csv(read_path:str):
    ''' 
    Read a csv file
    '''
    import csv
    with open(read_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            raise ValueError("The csv file is empty.")
        rows = list()
        for row in reader:
            rows.append(row)
    return rows