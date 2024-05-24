import streamlit as st
import pandas as pd
#import plotly.express as px

st.title('Gapminder')

st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

@st.cache_data
def load_and_preprocess_data():
    # Load the CSV files
    population = pd.read_csv('population.csv')
    life_expectancy = pd.read_csv('life_expectancy.csv')
    gni_per_capita = pd.read_csv('gni_per_capita.csv')

    # Forward fill missing values
    population.ffill(inplace=True)
    life_expectancy.ffill(inplace=True)
    gni_per_capita.ffill(inplace=True)

    # Melt dataframes to tidy format
    population_tidy = population.melt(id_vars=['country'], var_name='year', value_name='population')
    life_expectancy_tidy = life_expectancy.melt(id_vars=['country'], var_name='year', value_name='life_expectancy')
    gni_per_capita_tidy = gni_per_capita.melt(id_vars=['country'], var_name='year', value_name='gni_per_capita')

    # Merge the dataframes
    df_merged = population_tidy.merge(life_expectancy_tidy, on=['country', 'year'])
    df_merged = df_merged.merge(gni_per_capita_tidy, on=['country', 'year'])

    return df_merged

# Load and preprocess the data
data = load_and_preprocess_data()

# Display the data
st.write(data)

