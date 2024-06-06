from matplotlib import axis
import pandas as pd

def value2asr(data, axes:list[str], y_axis:str):
    data_new = pd.DataFrame()
    data_clean = data[data['adv_type'] == 'Clean']
    for row in data.iloc:
        if row['adv_type'] == 'Clean':
            continue
        filter_benchmark = data_clean['benchmark'] == row['benchmark']
        filter_model = data_clean['model_name'] == row['model_name']
        data_new = pd.concat([data_new, pd.DataFrame(
            {axis: row[axis] for axis in axes}
            | {'ASR': 1 - row[y_axis]/data_clean[filter_benchmark & filter_model][y_axis].values}
        )])
    return data_new