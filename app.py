import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import folium

st.set_option('deprecation.showPyplotGlobalUse', False)

# Step 1: Import the CSV file using pandas
st.title('Museum Data Analysis')
st.header('Step 1: Importing and Exploring the Data')
data = pd.read_csv('museum_data.csv')

# Explore the data
st.subheader('Exploring the Data')
st.write(data.head())
st.write(data.describe())

# Step 2: Data Cleaning
st.header('Step 2: Data Cleaning')
st.subheader('Removing Unnecessary Columns')
data.drop(['Locale Code (NCES)',
           'County Code (FIPS)', 'State Code (FIPS)',
           'Region Code (AAM)', 'Employer ID Number',
           'Tax Period'], axis=1, inplace=True)

st.subheader('Cleaned Data')
st.write(data.head())

# Check for missing or empty data
missing_data = data.isnull().sum()
st.subheader('Missing Data')
st.write(missing_data)

# Step 3: Data Summarization and Statistics
st.header('Step 3: Data Summarization and Statistics')
st.subheader('Total Number of Museums')
total_museums = len(data)
st.write(total_museums)

st.subheader('Different Types of Museums')
museum_types = data['Museum Type'].value_counts()
st.write(museum_types)

st.subheader('Average Income and Revenue')
average_income = data['Income'].mean()
average_revenue = data['Revenue'].mean()
st.write('Average income:', average_income)
st.write('Average revenue:', average_revenue)

# Step 4: Data Visualization
st.header('Step 4: Data Visualization')

st.subheader('Bar Chart for Distribution of Museums by Type')
plt.figure(figsize=(10, 6))
museum_types.plot(kind='bar')
plt.title('Distribution of Museums by Type')
plt.xlabel('Museum Type')
plt.ylabel('Count')
st.pyplot()

st.subheader('Pie Chart to Show Proportion of Museums in Each State')
plt.figure(figsize=(50, 20))
state_counts = data['State (Administrative Location)'].value_counts()
state_counts.plot(kind='pie', autopct='%1.1f%%')
plt.title('Proportion of Museums in Each State')
plt.ylabel('')
st.pyplot()

st.subheader('Scatter Plot to Display the Relationship between Income and Revenue')
plt.figure(figsize=(10, 6))
plt.scatter(data['Income'], data['Revenue'])
plt.title('Relationship between Income and Revenue')
plt.xlabel('Income')
plt.ylabel('Revenue')
st.pyplot()

plt.figure(figsize=(10, 6))
plt.scatter(data['Income'] / 1e6, data['Revenue'] / 1e6)  # Divide by 1e6 to convert to millions
plt.title('Relationship between Income and Revenue')
plt.xlabel('Income (Millions)')
plt.ylabel('Revenue (Millions)')
st.pyplot()

# Create a map centered around the mean latitude and longitude
st.subheader('Map of Museums by Type')
df = pd.read_csv("museum_data.csv")

# Drop the rows with missing Latitude and Longitude values
df = df.dropna(subset=['Latitude', 'Longitude'])

# Rename the columns to "lat" and "lon" for compatibility with st.map()
df = df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

# Define color mapping for different museum types
def color_mapping(museum_type):
    if museum_type == 'ARBORETUM' or museum_type == 'BOTANICAL GARDEN' or museum_type == 'NATURE CENTER':
        return '#339933'
    elif museum_type == 'ART MUSEUM':
        return '#993399'
    elif museum_type == 'CHILDREN\'S MUSEUM':
        return '#336699'
    elif museum_type == 'GENERAL MUSEUM' or museum_type == 'HISTORY MUSEUM':
        return '#FF9933'
    elif museum_type == 'HISTORIC PRESERVATION' or museum_type == 'NATURAL HISTORY MUSEUM':
        return '#CD5C5C'
    elif museum_type in ['SCIENCE & TECHNOLOGY MUSEUM', 'PLANETARIUM', 'AQUARIUM', 'WILDLIFE CONSERVATION']:
        return '#24AF3'
    else:
        return '#CCCCCC'

# Map the museum types to marker colors
df['color'] = df['Museum Type'].map(color_mapping)

# Select only the first 100 rows of the DataFrame
df = df.head(100)

# Display the map with markers colored by museum type
st.map(df[['lat', 'lon','color']])