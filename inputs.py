import streamlit as st
import pandas as pd

def ui_input():
    params = {}
    tables = []

    num_tables = st.selectbox('Select number of tables', [1, 2])
    params['num_tables'] = num_tables
    params['sample_data'] = True
    params['scale_factor'] = st.slider('Scale factor', min_value=1.0, max_value=10.0, value=1.0, step=0.1)

    if num_tables == 2:
        params['foreign_key'] = st.checkbox('Foreign keys', value=True)
        params['foreign_key_col'] = st.text_input('Enter foreign key column', value='PassengerId')
    else:
        params['foreign_key'] = False

    params['with_sample_tables'] = []
    for i in range(num_tables):
        with st.expander(f'Table {i+1}', expanded=True):
            name = st.text_input(f'Enter name of table {i+1}', value=f'DF{i+1}', key=f'table_name_{i}')
            params['with_sample_tables'].append({'name': name})

    if params['sample_data']:
        st.subheader("Upload Sample Data")

        for _ in range(num_tables):
            tables.append(None)

        for i, table in enumerate(params['with_sample_tables']):
            st.write(table['name'])
            key = f"file_uploader_{i}"
            uploaded_file = st.file_uploader(f"Choose a CSV file for {table['name']}", type=["csv"], key=key)
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                st.write(df)
                tables[i] = df

    return params, tables

def config_input():
    pass