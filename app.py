import streamlit as st
import pandas as pd
import math

# Function to allow user to upload a CSV file
def upload_csv():
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    
def assign_category(value):
    if value >= 1 and value <= 50:
        return 1
    elif value >= 51 and value <= 100:
        return 2
    elif value >= 101 and value <= 150:
        return 3
    elif value >= 151 and value <= 200:
        return 4
    elif value >= 201 and value <= 250:
        return 5
    else:
        return 6
    
def assign_type(value):
    if value >= 1 and value <= 50:
        return 'dog'
    elif value >= 51 and value <= 100:
        return 'cat'
    elif value >= 101 and value <= 150:
        return 'horse'
    elif value >= 151 and value <= 200:
        return 'monkey'
    elif value >= 201 and value <= 250:
        return 'panda'
    else:
        return 'fish'
    
def calculate_datapoints(value):
    datapoints = math.ceil(value/4)
    return datapoints
    
def process_data(markers):
    markers['opensesame_time'] = pd.to_datetime(markers['datetime'])
    markers['BESS_time'] = pd.to_datetime(markers['BESS_time'])
    markers['milliseconds_opensesame'] = markers['opensesame_time'].dt.hour * 3600000 + markers['opensesame_time'].dt.minute * 60000 + markers['opensesame_time'].dt.second * 1000
    markers['milliseconds_BESS'] = markers['BESS_time'].dt.hour * 3600000 + markers['BESS_time'].dt.minute * 60000 + markers['BESS_time'].dt.second * 1000
    markers['onset_miliseconds'] = markers['time_image'] - (markers['milliseconds_BESS']-markers['milliseconds_opensesame'])
    markers['onset_relaxation_miliseconds'] = markers['time_relaxation'] - (markers['milliseconds_BESS']-markers['milliseconds_opensesame'])
    markers['class'] = markers['count'].apply(lambda x: assign_category(x))
    markers_required = markers[['count','time_fixation','time_image','time_relaxation','milliseconds_BESS','milliseconds_opensesame','onset_miliseconds','onset_relaxation_miliseconds','class']]
    st.write(markers_required.head())
    markers_required['data_points'] = markers_required['onset_miliseconds'].apply(lambda x: calculate_datapoints(x))
    markers_required['data_points_relaxation'] = markers_required['onset_relaxation_miliseconds'].apply(lambda x: calculate_datapoints(x))
    st.write(markers_required)

# Function to select relevant columns
def select_columns(data):
    st.subheader("Select Relevant Columns")
    all_columns = data.columns.tolist()
    selected_columns = st.multiselect("Select columns", all_columns,default=all_columns)
    if selected_columns:
        selected_data = data[selected_columns]
        process_data(selected_data)
        # st.write(selected_data.head())

def main():
    st.title("CSV File Upload and Column Selection App")
    
    # Upload CSV file
    data = upload_csv()
    
    if data is not None:
        datetime = data['datetime'][0]
        st.write("Opensesame Datetime")
        st.write(datetime)
        bess_time = st.text_input("Enter BESS time", value=datetime)
        data['BESS_time'] = pd.to_datetime(bess_time)
        st.write(data)
        st.write(data.isna().sum())
        select_columns(data)

if __name__ == "__main__":
    main()
