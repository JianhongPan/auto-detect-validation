import os

def save_to_csv(save_path:str, **row):
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
            writer.writerow([*row.keys()])
        # check if the fields in the header exist in the row
        elif any(key not in row for key in header):
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
            return list()
        rows = list()
        for row in reader:
            rows.append(row)
    return rows

def filter_logs(logs:list, *fields):
    logs = [log for log in logs if all(field in log for field in fields)]
    return logs

def get_current_time():
    ''' 
    Get the current time
    '''
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")