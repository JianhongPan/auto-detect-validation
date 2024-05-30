import os
import re
import subprocess
import yaml
from csv_tools import save_to_csv, read_from_csv
from unittest import result

def get_config_list():

    # load the name of candidate model for evaluation
    yml_path = 'model_list.yml'
    if os.path.exists(yml_path):
        with open(yml_path, 'r') as f:
            model_list = yaml.safe_load(f)

    # load the model's config for evaluation
    config_list = list()
    # create a directory to save config and checkpoint files
    if not os.path.exists('checkpoints'):
        os.mkdir('checkpoints')

    # list all the available models
    config_dir_path = os.path.join('mmdetection', 'configs')
    for model_name in os.listdir(config_dir_path):
        config_path = os.path.join(config_dir_path, model_name)
        yml_path = os.path.join(config_path, 'metafile.yml')
        if os.path.exists(yml_path):
            with open(yml_path, 'r') as f:
                config = yaml.safe_load(f)
                # print all the submodels
                if 'Models' in config:
                    config = config['Models']
                for submodel in config:
                    if submodel['Name'] not in model_list:
                        continue
                    submodel['model_config_path'] = os.path.join(config_path, submodel['Name'] + '.py')
                    config_list.append(submodel)

    return config_list
    
def get_checkpoint_path(model):
    checkpoint_path = os.path.join('mmdetection', 'checkpoints', model["Name"] + '.pth')
    checkpoint_hash_path = os.path.join('mmdetection', 'checkpoints', model["Name"] + '.md5')
    checkpoint_url = model["Weights"]
    if os.path.exists(checkpoint_path) and os.path.exists(checkpoint_hash_path):
        # get the hash of the local model
        current_model_hash = subprocess.run(['md5sum', checkpoint_path], stdout=subprocess.PIPE).stdout.decode().split()[0]
        with open(checkpoint_hash_path, 'r') as f:
            model_hash = f.read().strip()
        if current_model_hash == model_hash:
            return checkpoint_path

    print(f"Downloading the checkpoint of the model {model['Name']}...")
    try:
        subprocess.run(['wget', checkpoint_url, '-O', checkpoint_path], stdout=subprocess.PIPE).stdout.decode()
    except:
        print(f"Failed to download the checkpoint of the model {model['Name']}.")
    # get the hash of the downloaded model
    model_hash = subprocess.run(['md5sum', checkpoint_path], stdout=subprocess.PIPE).stdout.decode().split()[0]
    with open(checkpoint_hash_path, 'w') as f:
        f.write(model_hash)
    return checkpoint_path

def get_dataset_list(data_path):
    dataset_list = list()
    for dataset_name in os.listdir(data_path):
        dataset_path = os.path.join(data_path, dataset_name)
        if os.path.isdir(dataset_path):
            dataset_list.append({'Name': dataset_name, 'Path': dataset_path})
    return dataset_list

def filter_logs(logs:list, *fields):
    logs = [log for log in logs if all(field in log for field in fields)]
    return logs

def test_model(model, dataset):
    print(f"Testing the model {model['Name']} on the dataset {dataset['Name']}...")
    model_config_path = os.path.realpath(model['model_config_path'])
    model_checkpoint_path = os.path.realpath(get_checkpoint_path(model))
    dataset_path = dataset['Path']

    # remove all the existing symbol links in the data/coco directory
    for file_name in os.listdir(os.path.join('mmdetection', 'data', 'coco')):
        file_path = os.path.join('mmdetection', 'data', 'coco', file_name)
        if os.path.islink(file_path):
            os.unlink(file_path)

    # create symbol links of all the files in the given dataset in data/coco
    for file_name in os.listdir(dataset_path):
        file_path = os.path.join(dataset_path, file_name)
        file_path = os.path.realpath(file_path)
        link_path = os.path.join('mmdetection', 'data', 'coco', file_name)
        os.symlink(file_path, link_path)

    print(f"Testing the model {model['Name']}...")
    subprocess_instance = subprocess.run(['python', os.path.join('tools', 'test.py'), model_config_path, model_checkpoint_path], stdout=subprocess.PIPE, cwd='mmdetection')
    output = subprocess_instance.stdout.decode().splitlines()
    print(output)
    # get the test results
    try:
        result = {
            'mAP_50_95': filter_logs(output, 'Average Precision', 'area=   all')[0].split()[-1],
            'mAP_50': filter_logs(output, 'Average Precision', 'area=   all')[1].split()[-1],
            'mAP_75': filter_logs(output, 'Average Precision', 'area=   all')[2].split()[-1],
            'mAR_50_95': filter_logs(output, 'Average Recall', 'area=   all')[0].split()[-1]
        }
        return result
    except:
        raise ValueError("The test results are not correct.")

def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Test the models')
    parser.add_argument('--data-path', default='dataset', type=str, help='The path to all the datasets')
    parser.add_argument('--gpu', default=1, type=int, help='The number of GPUs to use')

    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()

    config_list = get_config_list()
    dataset_list = get_dataset_list(args.data_path)

    for model in config_list:
        print(model['Name'])
        for dataset in dataset_list:
            actor_type, adv_type, benchmark = dataset['Name'].split('_')
            result_fields = {
                'actor_type': actor_type,
                'adv_type': adv_type,
                'benchmark': benchmark,
                'model_name': model['Name']
            }

            try:
                # check if the model has been tested on the dataset
                rows = read_from_csv('results.csv')
                result_field_list = [row[:len(result_fields)] for row in rows]
                if [*result_fields.values()] in result_field_list:
                    print(f"The model {model['Name']} has been tested on the dataset {dataset['Name']}.")
                    continue

                # test the model
                result = test_model(model, dataset)

                # save the results to a csv file
                save_to_csv('results.csv', **result_fields, **result)
            except Exception as ValueError:
                print(f"Error: {ValueError} in testing the model {model['Name']}")
                continue
