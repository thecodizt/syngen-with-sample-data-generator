import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm

def generate_plot(table_data, selected_column):
    if pd.api.types.is_numeric_dtype(table_data[selected_column]):
        # For numeric columns, generate a histogram, box plot, and line plot
        fig_histogram = px.histogram(table_data, x=selected_column, title=f"{selected_column} - Histogram")
        fig_boxplot = px.box(table_data, y=selected_column, title=f"{selected_column} - Box Plot")
        fig_lineplot = px.line(table_data, x=table_data.index, y=selected_column, title=f"{selected_column} - Line Plot")
        
        # Set dimensions for the plots
        fig_histogram.update_layout(width=500, height=400)
        fig_boxplot.update_layout(width=500, height=400)
        fig_lineplot.update_layout(width=500, height=400)
        
        st.plotly_chart(fig_histogram)
        st.plotly_chart(fig_boxplot)
        st.plotly_chart(fig_lineplot)
    elif pd.api.types.is_datetime64_any_dtype(table_data[selected_column]):
        # For date columns, generate a time series plot
        fig_timeseries = px.line(table_data, x=table_data.index, y=selected_column, title=f"{selected_column} - Time Series Plot")
        
        # Set dimensions for the plot
        fig_timeseries.update_layout(width=500, height=400)
        
        st.plotly_chart(fig_timeseries)
    else:
        # For categorical columns, generate a bar chart
        value_counts = table_data[selected_column].value_counts()
        fig_bar = px.bar(x=value_counts.index, y=value_counts.values, title=f"{selected_column} - Bar Chart")
        
        # Set dimensions for the plot
        fig_bar.update_layout(width=500, height=400)
        
        st.plotly_chart(fig_bar)
        
def generate_description(table, column):
    np_series = table[column]
    
    # Check the datatype of the column
    if np_series.dtype == 'object':  # Assuming 'object' dtype represents categorical data
        value_counts = np_series.value_counts()
        st.write("Value Counts:")
        st.write(value_counts)
    elif np.issubdtype(np_series.dtype, np.number):  # Check if the column contains numerical data
        mean = np.mean(np_series)
        median = np.median(np_series)
        std_dev = np.std(np_series)
        min_val = np.min(np_series)
        max_val = np.max(np_series)

        st.write("Mean:", mean)
        st.write("Median:", median)
        st.write("Standard Deviation:", std_dev)
        st.write("Minimum Value:", min_val)
        st.write("Maximum Value:", max_val)
        
        # Calculate slope
        x = np.arange(len(np_series))
        slope, intercept = np.polyfit(x, np_series, 1)
        st.write("Slope:", slope)
        
    elif np_series.dtype == 'datetime64[ns]':  # Check if the column contains datetime data
        min_date = np.min(np_series)
        max_date = np.max(np_series)
        st.write("Minimum Date:", min_date)
        st.write("Maximum Date:", max_date)
    
    else:
        try:
            # For object columns, generate a bar chart
            value_counts = table[column].astype(str).value_counts()
            st.write(value_counts)
            fig_bar = px.bar(x=value_counts.index, y=value_counts.values, title=f"{column} - Bar Chart")
            
            # Set dimensions for the plot
            fig_bar.update_layout(width=500, height=400)
            
            st.plotly_chart(fig_bar)
        
        except ValueError:
            st.write("Unsupported data type. Please provide a column with numerical, categorical, or date data.")
        
def visualize(table):
    
    for col in table.columns:
        with st.expander(f"{col}"):
            generate_plot(table, col)
    
    # generate_description(table, selected_column)