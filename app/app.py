#----------------------------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import re
#----------------------------------------------------------------------------------------------------------------------
st.title('Gapminder')

st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

st.write("Made by the efforts of Freddy Mercado for his Enterprise Architechtures for Big Data course")
#----------------------------------------------------------------------------------------------------------------------
@st.cache_data
def load_and_preprocess_data(population_file, life_expectancy_file, gni_per_capita_file):

    population = pd.read_csv(population_file)
    population.ffill(inplace=True)
    population_tidy = population.melt(id_vars=['country'], var_name='year', value_name='population')

    life_expectancy = pd.read_csv(life_expectancy_file)
    life_expectancy.ffill(inplace=True)
    life_expectancy_tidy = life_expectancy.melt(id_vars=['country'], var_name='year', value_name='life_expectancy')

    gni_per_capita = pd.read_csv(gni_per_capita_file)
    gni_per_capita.ffill(inplace=True)
    gni_per_capita_tidy = gni_per_capita.melt(id_vars=['country'], var_name='year', value_name='gni_per_capita')

    df_merged = population_tidy.merge(life_expectancy_tidy, on=['country', 'year'])
    df_merged = df_merged.merge(gni_per_capita_tidy, on=['country', 'year'])

    return df_merged

def convert_population(population):
    if pd.isnull(population):
        return population
    
    # Check for 'B' or 'b' suffix for billion
    if re.search(r'[Bb]$', population):
        return float(population[:-1]) * 1e9
    
    # Check for 'M' or 'm' suffix for million
    elif re.search(r'[Mm]$', population):
        return float(population[:-1]) * 1e6
    
    # Check for 'k' suffix for thousand
    elif re.search(r'k$', population):
        return float(population[:-1]) * 1e3
    
    # Return as is for other cases
    else:
        return float(population)


st.title('Gapminder Data Dashboard')
st.write('This dashboard displays data for Population, Life Expectancy, and GNI per Capita.')

# Upload the CSV files
population_file = st.file_uploader('Upload Population CSV', type='csv')
life_expectancy_file = st.file_uploader('Upload Life Expectancy CSV', type='csv')
gni_per_capita_file = st.file_uploader('Upload GNI per Capita CSV', type='csv')

# Ensure all files are uploaded
if population_file and life_expectancy_file and gni_per_capita_file:
    # Load and preprocess the data
    data = load_and_preprocess_data(population_file, life_expectancy_file, gni_per_capita_file)
    
    # Convert year to integer for proper slider functionality
    data['year'] = data['year'].astype(int)

    # Interactive widgets
    year_slider = st.slider('Select Year', min_value=int(data['year'].min()), max_value=int(data['year'].max()), value=int(data['year'].min()), step=1)
    countries = st.multiselect('Select Countries', options=data['country'].unique(), default=data['country'].unique())

    # Filter data based on selections
    filtered_data = data[(data['year'] == year_slider) & (data['country'].isin(countries))]

    # Filter out invalid values for GNI per capita
    filtered_data = filtered_data.dropna(subset=['gni_per_capita'])

    # Convert 'gni_per_capita' to numeric type and filter out invalid values
    filtered_data['gni_per_capita'] = pd.to_numeric(filtered_data['gni_per_capita'], errors='coerce').dropna()

    # Apply logarithmic transformation to GNI per capita
    filtered_data['log_gni_per_capita'] = np.log(filtered_data['gni_per_capita'])

    # Convert population values
    filtered_data['population'] = filtered_data['population'].apply(convert_population)

    # Create bubble chart
    fig = px.scatter(filtered_data, 
                     x='log_gni_per_capita', 
                     y='life_expectancy', 
                     size='population', 
                     color='country', 
                     hover_name='country',
                     size_max=60, 
                     labels={'log_gni_per_capita': 'Log GNI per Capita', 'life_expectancy': 'Life Expectancy'},
                     title=f'Bubble Chart for the Year {year_slider}')

    # Set x-axis range
    x_min = filtered_data['log_gni_per_capita'].min()
    x_max = filtered_data['log_gni_per_capita'].max()
    fig.update_layout(xaxis=dict(title='Log GNI per Capita', range=[x_min, x_max]))

    # Display bubble chart
    st.plotly_chart(fig)
else:
    st.write('Please upload all three CSV files.')

