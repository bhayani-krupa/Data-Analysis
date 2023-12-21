import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def load_data():
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.session_state.data = data  # Store data in session state
        st.write(data)
    else:
        st.write("Please upload a CSV file.")

import pandas as pd
import streamlit as st

def clean_data():
    if 'data' in st.session_state:  # Check if data is in session state
        data = st.session_state.data  # Retrieve data from session state

        # Remove duplicate values
        # data = data.drop_duplicates()
        # st.write("Duplicate values removed.")
        
        st.markdown("<h1 style='text-align: center; color: red;'>Data Cleaning Options</h1>", unsafe_allow_html=True)

        st.markdown("""
        1. Show number of null values
        2. Fill null values

        """, unsafe_allow_html=True)

    option = st.selectbox("Choose an option", ("Show number of null values",  "Fill null values"))

        
    if option == "Show number of null values":
            st.write(data.isnull().sum())
            
    elif option == "Fill null values":
            # Select column to replace null values
            fill_option = st.selectbox("Choose a method to fill null values", ("Drop","Drop Column", "Mean", "Median"))

            
            if fill_option == "Drop":
                column_selected = st.selectbox("Select the column to replace null values:", data.columns)
                data = data[column_selected].dropna()
                st.write(data)
                return(data)
            elif fill_option == "Drop Column":
                columns_selected = st.multiselect("Select the column to delete:", data.columns)
                data1 = data.drop(columns_selected, axis=1)
                st.write(data1)  
                return(data)                 
            elif fill_option == "Mean":
                column_selected = st.selectbox("Select the column to replace null values:", data.columns)               
                data = data[column_selected].fillna(data[column_selected].mean())
                st.write(data)  
                return(data)   
            elif fill_option == "Median":
                column_selected = st.selectbox("Select the column to replace null values:", data.columns)
                data = data[column_selected].fillna(data[column_selected].median())
                st.write(data)  
                return(data)
    else:
        st.write("No data to clean.")


def explore_data():
    if 'data' in st.session_state:  # Check if data is in session state
        data = st.session_state.data  # Retrieve data from session state

        column_selected = st.selectbox("Select a numeric column", data.select_dtypes(include='number').columns)

        st.subheader("Some general statistics are")
        # st.write("Mean is", data[column_selected].mean())
        st.write("Mean ",data[column_selected].mean())
        st.write("Median is", data[column_selected].median())
        st.write("Mode is", data[column_selected].mode().iloc[0])
        st.write("Range is",(data[column_selected].max()-data[column_selected].min()))
        st.write("Midrange is",(data[column_selected].max()-data[column_selected].min())/2)

        st.write("All 3 quartiles are")
        st.write(data[column_selected].quantile([0.25,0.5,0.75]))
        st.write("The interquartile range is", data[column_selected].quantile(0.75)-data[column_selected].quantile(0.25))
        st.write("Standard Deviation is", data[column_selected].std())
        st.write("Variance is", data[column_selected].var())

        data.boxplot(column_selected)

        # #outliers dropped
        # q1, q3 = np.quantile(data[column_selected], [0.25, 0.75])
        # # Calculate the interquartile range
        # iqr = q3 - q1
        # # Calculate the lower and upper bounds
        # lower_bound = q1 - (1.5 * iqr)
        # upper_bound = q3 + (1.5 * iqr)
        # clean_data = data[(data[column_selected] >= lower_bound) & (data[column_selected] <= upper_bound)]
        # clean_data.boxplot(column_selected)
# Allow user to select at least two numeric columns for correlation heatmap
        columns_selected = st.multiselect("Select numeric columns for correlation heatmap:", data.select_dtypes(include='number').columns)
        if len(columns_selected) >= 2:
# Display correlation heatmap for selected columns
            st.subheader("Correlation Heatmap")
            correlation_matrix = data[columns_selected].corr()
            fig, ax = plt.subplots()
            sns.heatmap(correlation_matrix, annot=True, cmap="viridis", center=0, ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Please select at least two numeric columns for the correlation heatmap.")


def plot_graph():
    if 'data' in st.session_state:
        data = st.session_state.data

        # User selects the type of graph
        graph_type = st.selectbox("Select the type of graph", ('Bar plot', 'Line plot', 'Scatter plot', 'Box plot', 'Pie chart', 'Histogram'))

        # User selects at least one column for visualization
        selected_columns = st.multiselect("Select columns for visualization", data.columns)

        if not selected_columns:
            st.warning("Please select at least one column for visualization.")
            return

        # Convert data to numeric if needed
        for col in selected_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')

        # Plot the selected graph
        fig, ax = plt.subplots()

        if graph_type == 'Bar plot':
            # Improve performance by limiting the number of bars in the bar plot
            if len(selected_columns) > 10:
                st.warning("Too many columns selected for a bar plot. Consider selecting fewer columns.")
                return
            data[selected_columns].plot(kind='bar', ax=ax)
            st.pyplot(fig)
        elif graph_type == 'Line plot':
            data[selected_columns].plot(kind='line', ax=ax)
            st.pyplot(fig)
        elif graph_type == 'Scatter plot':
            if len(selected_columns) >= 2:
                plt.scatter(data[selected_columns[0]], data[selected_columns[1]])
                st.pyplot(fig)
            else:
                st.warning("Please select at least two columns for scatter plot.")
                return
        elif graph_type == 'Box plot':
            data[selected_columns].boxplot(ax=ax)
            st.pyplot(fig)
        elif graph_type == 'Pie chart':
            if len(selected_columns) == 1:
                data[selected_columns[0]].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
                st.pyplot(fig)
            else:
                st.warning("Pie chart requires a single column. Select only one column for visualization.")
                return
        elif graph_type == 'Histogram':
            if len(selected_columns) >= 2:
                st.subheader("Histogram")
                fig, ax = plt.subplots()
                data[selected_columns].hist(ax=ax, bins=20, alpha=0.7)
                ax.set_title(f"Combined Histogram for {', '.join(selected_columns)}")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            else:
                st.warning("Please select at least two columns for a combined histogram.")
                return
    else:
        st.write("No data to visualize.")

def main():
    st.sidebar.title("Menu")
    menu = ["Home", "Upload Data", "Clean Data", "Explore Data", "Visualize Data"]
    choice = st.sidebar.selectbox("Choose an option", menu)
    data = None
    if choice == "Home":
        st.subheader("DWM MINIPROJECT")
        st.write("Krupa Bhayani - 60003210184")
        st.write("Bhavya Majani - 60003210168")
        st.write()
        st.write("Welcome to the data processing app!")
    elif choice == "Upload Data":
        st.subheader("Upload your CSV data")
        load_data()
    elif choice == "Clean Data":
        st.subheader("Clean your data")
        clean_data()
    
    elif choice == "Explore Data":
        st.subheader("Explore your data")
        explore_data()
    elif choice == "Visualize Data":
        st.subheader("Visualize your data")
        plot_graph()

if __name__ == "__main__":
    main()
