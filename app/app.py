import streamlit as st
import pandas as pd
#import plotly.express as px

# --------------------------------------- Step 01: Pre processing the data -------------------------------------------

st.title('Gapminder')

st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

st.write("Made by the efforts of Freddy Mercado for his Enterprise Architechtures for Big Data course")

import streamlit as st
import pandas as pd

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

st.title('Gapminder Data Dashboard')
st.write('This dashboard displays data for Population, Life Expectancy, and GNI per Capita.')
st.write("Please upload the necessary datasets for this webpage to function")

# Upload the CSV files
population_file = st.file_uploader('Upload Population CSV', type='csv')
life_expectancy_file = st.file_uploader('Upload Life Expectancy CSV', type='csv')
gni_per_capita_file = st.file_uploader('Upload GNI per Capita CSV', type='csv')

# Ensure all files are uploaded
if population_file and life_expectancy_file and gni_per_capita_file:
    # Load and preprocess the data
    data = load_and_preprocess_data(population_file, life_expectancy_file, gni_per_capita_file)
    
    # Display the data
    st.write('## Data Overview')
    st.write(data)
else:
    st.write('Please upload all three CSV files.')

