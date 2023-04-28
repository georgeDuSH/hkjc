import os, argparse
from itertools import product
import pandas as pd
import numpy as np


parser = argparse.ArgumentParser(description='GridSearch')
parser.add_argument('--model_name')
parser.add_argument('--result_path', default='')
parser.add_argument('--train_file_path', default='/Users/2ee8/Subject/hku/s2/STAT8017/hkjc_race_ranking/horse/ml_train.py')
args = parser.parse_args()
models = { "logistic":{
                    'penalty' : ['l2'],
                    'solver' : ['lbfgs'],
                    'max_iter' : [1000, 5000, 500],
                    'C': [0.1,1,0.1]
                        },
            "dtc":{
                    'criterion' : ['gini', 'entropy', 'log_loss'],
                    'splitter' : ['best', 'random'],
                    'max_depth' : [2, 20, 1], # int
                    'min_samples_leaf' : [2, 10, 1], #int and float
                    'min_samples_split' : [2, 10, 1]
                    },
            "rfc":{
                    'criterion' : ['gini', 'entropy', 'log_loss'],
                    'max_depth' : [2, 3, 1], # int
                    'min_samples_leaf' : [2, 3, 1], #int and float
                    'min_samples_split' : [2, 3, 1], #int and float
            },
            "adc":{
                    'n_estimators' : [50, 60, 10], # int
                    'learning_rate' : [5e-5, 5e-4, 1e-1], # float
                    'algorithm' : ['SAMME', 'SAMME.R'],
            },
            "ridge":{
                'alpha' : [0.01, 1, 0.01], # float
                'solver' : ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga', 'lbfgs'],
            },
            "dtr":{
                    'criterion' : ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'splitter' : ['best', 'random'],
                    'max_depth' : [2, 20, 1], # int
                    'min_samples_leaf' : [2, 10, 1], #int and float
                    'min_samples_split' : [2, 10, 1], #int and float
            },
            "rfr":{
                    'criterion_reg' : ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'max_depth' : [2, 20, 1], # int
                    'min_samples_leaf' : [2, 10, 1], #int and float
                    'min_samples_split' : [2, 10, 1], #int and float
            },
            "adr":{
                    'n_estimators' : [50, 5000, 10], # int
                    'learning_rate' : [5e-5, 1e-1, 1e-1], # float
                    'loss' : ['linear', 'square', 'exponential']
            },
            "xgbc":{
                'colsample_bytree' : [0.5, 0.8, 0.1], # float
                'reg_alpha' : [0.0001, 0.0002, 1], # float
                'reg_lambda' : [0.0001, 0.0002, 1], # float
                'max_depth' : [2, 20, 1], # int
                'min_child_weight' : [1, 10, 1], # float
                'subsample' : [0.5, 0.8, 0.1], # float
                'n_estimators' : [50, 5000, 10], # int
                'learning_rate' : [5e-4, 1e-1, 5e-1], # float
            },
            "xgbr":{
                'colsample_bytree' : [0.5, 0.8, 0.1], # float
                'reg_alpha' : [0.0001], # float
                'reg_lambda' : [0.0001], # float
                'min_child_weight' : [1, 10, 1], # float
                'subsample' : [0.5, 0.8, 0.1], # float
                'n_estimators' : [50, 5000, 10], # int
                'learning_rate' : [5e-5, 1e-1, 1e-1], # float
                'max_depth' : [2, 20, 1]
            }
}



def range_to_list(range_list):
    return [x for x in np.arange(range_list[0], range_list[1], range_list[-1])]

def get_result(model:str):
    print('Training {}....'.format(model))
    for model_name in models.keys():
        if model_name == model:
            result = {'AP':[]}
            temp = []
            for params_name in models[model_name].keys():
                result[params_name] = []
                if isinstance(models[model_name][params_name][0], str):
                    temp.append(models[model_name][params_name])
                else:
                    temp.append(range_to_list(models[model_name][params_name]))
            combinations = product(*temp)
            keys = [key for key in models[model_name].keys()]
            for combine in combinations:
                cmd = 'python {} --model {}'.format(args.train_file_path, model_name)
                count = 0
                temp = {}
                for key in keys:
                    temp[key] = []
                for value in combine:
                    cmd += ' --{paramname} {paramvalue}'.format(paramname=keys[count],paramvalue=value)
                    result[keys[count]].append(value)
                    count += 1
                print(cmd)
                cmd_result = os.popen(cmd)
                #print(cmd_result.readlines())
                ap = cmd_result.readlines()[1].split(':')[-1].strip()
                result['AP'].append(ap)
            print(result)
        else:
            continue
    pd.DataFrame.from_dict(result).to_csv('{}{}.csv'.format(args.result_path, model))


get_result(args.model_name)