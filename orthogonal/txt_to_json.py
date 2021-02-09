# -*- coding: utf-8 -*-

import pandas as pd
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def build_json():
    with open(dir_path + r'/orthogonal_arrays.txt') as file:
        text = file.read()
    chunks = text[1:].split('\n\n\n')
    
    arrays = []

    for chunk in chunks:
        
        try:

            name = chunk.split('\n')[0]

            lines = chunk.split('\n')[1:]

            groups = [g for g in name.split('n')[0].split(' ') if g is not '']

            lengths = []
            for g in groups:
                for i in range(int(g.split('^')[1])):
                    lengths.append(len(g.split('^')[0]))

            i = 0
            slices = []
            for l in lengths:
                slices.append(slice(i, i+l))
                i += l

            array = []

            for line in lines:

                array.append([int(line[s].replace(' ', '')) for s in slices])

            exponents = name.split('n')[0]
            runs = int(name.split('n=')[-1])

            array_dict = {
                'array': json.dumps(array),
                'runs': runs
            }
            exp_dict = {}

            for exp_group in exponents.split(' '):
                try: 
                    key, exp = exp_group.split('^')
                    exp_dict[int(key)] = int(exp)
                except ValueError: # ValueError
                    pass
            array_dict.update(exp_dict)
            array_dict['exponents'] = exp_dict
            arrays.append(array_dict)
        except:
            print(name)
            pass

    base = pd.DataFrame([pd.Series(array) for array in arrays]).fillna(0)
    int_columns = sorted([c for c in base.columns if type(c) is int])
    string_columns = [c for c in base.columns if type(c) is str]
    base[int_columns] = base[int_columns].astype(int)

    base = base[string_columns + int_columns] 

    base.sort_values(['runs'] + int_columns, inplace=True)
    base.reset_index(inplace=True, drop=True)
    base['len'] = base['array'].apply(lambda s: len(json.loads(s)))
    base['error'] = (base['len'] - base['runs'])

    with open(dir_path + r'/orthogonal_arrays.json', 'w') as file:
        file.write(base.to_json(orient='records'))


def try_int(s):
    try: 
        return int(s)
    except ValueError: 
        return s


