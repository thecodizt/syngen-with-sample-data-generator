import streamlit as st

from methods.gan_generator import GAN
import pandas as pd

def generate(params, table):

    numeric_data = table.select_dtypes(include=['int64', 'float64'])

    non_numeric_data = table.select_dtypes(include=['object'])

    non_numeric_data_list = non_numeric_data.values.tolist()

    unique_records = set(tuple(x) for x in non_numeric_data_list)

    unique_records = list(unique_records)

    unique_records = [list(x) for x in unique_records]

    index_list = [unique_records.index(x) for x in non_numeric_data_list]

    non_numeric_data['_id'] = index_list

    numeric_data['_id'] = index_list

    table['_id'] = index_list

    int_data = table.select_dtypes(include=['int64'])
    int_columns = int_data.columns.values.tolist()
    numeric_columns = numeric_data.columns.values.tolist()

    num_generated_samples = int(params['scale_factor'] * len(table)) # should take from config file
    # randomness_degree = params['randomness_degree'] # should take from config file
    randomness_degree = 100
    gan_model = GAN(numeric_data, randomness_degree)
    generated_numeric_data = pd.DataFrame(gan_model.generate(num_generated_samples))
    
    generated_numeric_data.columns = numeric_columns

    for column in int_columns:
        generated_numeric_data[column] = generated_numeric_data[column].astype(int)

    result = pd.merge(generated_numeric_data, non_numeric_data, on='_id')

    print(num_generated_samples, len(generated_numeric_data), len(result), len(non_numeric_data))

    result.drop('_id', axis=1, inplace=True)
    table.drop('_id', axis=1, inplace=True)
    
    result = result.sample(int(params['scale_factor'] * len(table)))
    
    result.reset_index(inplace=True)
    result.drop('index', axis=1, inplace=True)

    return result