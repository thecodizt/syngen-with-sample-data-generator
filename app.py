import streamlit as st

from inputs import ui_input, config_input
from utils import analysis, merge_tables, split_tables, split_columns
from generate import generate
from visualize import visualize
import datetime

def with_sample_data_generator():
    st.title("With Sample Data Generator")
    
    with st.expander("Documentaion"):
        st.markdown("""
            # TBD            
        """)
        
    input_method = "UI"
    
    params = None
    tables = []

    if input_method == "UI":
        params, tables = ui_input()
        
        if params:
            st.subheader("Configuration")
            st.write(params)

    elif input_method == "YAML":
        pass

    generate_button = None

    if params is not None:
        if params['num_tables'] > 2 or params['num_tables'] < 1:
            st.error("Number of tables should be 1 or 2")
        else:
            generate_button = st.button("Generate")

    if params is not None and generate_button:

        original_data = None
        generated_data = None

        if params['sample_data']:

            if params['foreign_key']:
                table, df1_cols, df2_cols = merge_tables(params, tables)

                original_data = table

                st.subheader("Merged Data based on Foreign Key")

                st.write(table)

                st.header("Generated Data")

                generated_data = generate(params, table)
                
                # table = generated_data.sample(int(params['scale_factor']*len(original_data))).reset_index()

                st.write("Splitting the generated data into two tables")
                res1, res2 = split_columns(table, df1_cols)

                st.subheader("Table 1")
                st.write(res1)
                st.download_button(label="Download CSV", data=res1.to_csv().encode("utf-8"), file_name=f"generated_table_{datetime.datetime.now()}.csv", mime="text/csv")

                st.subheader("Table 2")
                st.write(res2)
                st.download_button(label="Download CSV", data=res2.to_csv().encode("utf-8"), file_name=f"generated_table_{datetime.datetime.now()}.csv", mime="text/csv")

                analysis(original_data, table)

            else:
                st.header("Generated Data")

                original_data = tables[0]

                table = generate(params, tables[0])
                
                # table = table.sample(int(params['scale_factor']*len(original_data))).reset_index()

                generated_data = table

                st.write(table)
                st.download_button(label="Download CSV", data=table.to_csv().encode("utf-8"), file_name=f"generated.csv", mime="text/csv")

        if original_data is not None and generated_data is not None:
            analysis(original_data, generated_data)
            
if __name__ == "__main__":
    with_sample_data_generator()