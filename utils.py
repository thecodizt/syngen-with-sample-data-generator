import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def split_tables(params, table, df1_cols, df2_cols):
    foreign_key = params['foreign_key_col']
    df = table

    df1 = df[df1_cols]
    df2 = df[df2_cols]

    # Set the foreign key as the index for each new DataFrame
    df1.set_index(foreign_key, inplace=True)
    df2.set_index(foreign_key, inplace=True)

    return [df1, df2]

def split_columns(df, split_columns):
    df1 = df[split_columns]
    df2 = df.drop(columns=split_columns)
    return df1, df2

def merge_tables(params, tables):
    df1 = tables[0]
    df2 = tables[1]

    df = pd.merge(df1, df2, on=str(params['foreign_key_col']))

    return df, df1.columns.values.tolist(), df2.columns.values.tolist()

def analysis(original_data, generated_data):
    st.header("Analysis")

    st.subheader("Statistics")
    with st.expander("Original Data"):
        st.write(original_data.describe())

    with st.expander("Generated Data"):
        st.write(generated_data.describe())

    st.subheader("Visualizations")

    # Visualize statistics for each column
    for column in original_data.columns:
        # Box plot
        with st.expander(f'{column}'):
            fig = go.Figure()
            fig.add_trace(go.Box(y=original_data[column], name='Original'))
            fig.add_trace(go.Box(y=generated_data[column], name='Generated'))
            fig.update_layout(title_text=column, autosize=False, width=800, height=500)
            st.plotly_chart(fig, use_container_width=True)

    
            if original_data[column].dtype == 'object':
                st.subheader(f'Histogram for {column}')
                fig = go.Figure()
                fig.add_trace(go.Histogram(x=original_data[column], name='Original', opacity=0.75))
                fig.add_trace(go.Histogram(x=generated_data[column], name='Generated', opacity=0.75))
                fig.update_layout(title_text=column, barmode='overlay', autosize=False, width=800, height=500)
                st.plotly_chart(fig, use_container_width=True)
            # # If the column is numeric, use scatter plot
            # else:
            #     st.subheader(f'Scatter plot for {column}')
            #     fig = go.Figure()
            #     fig.add_trace(go.Scatter(x=original_data[column], y=generated_data[column], mode='markers', name='Original'))
            #     fig.add_trace(go.Scatter(x=generated_data[column], y=generated_data[column], mode='markers', name='Generated'))
            #     fig.update_layout(title_text=column, autosize=False, width=800, height=500)
            #     st.plotly_chart(fig, use_container_width=True)

