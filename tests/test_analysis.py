import pandas as pd
import numpy as np
import pytest
from data_analysis import analysis

# sztuczny df alkoholu
@pytest.fixture
def alcohol_df():
    return pd.DataFrame({
        'Województwo': ['mazowieckie', 'małopolskie', 'mazowieckie'],
        'Numer zezwolenia': [1, 2, 3]
    })

@pytest.fixture
def fire_df():
    return pd.DataFrame({
        'Województwo': ['mazowieckie', 'małopolskie', 'mazowieckie'],
        'OGÓŁEM Liczba zdarzeń': [10, 5, 15]
    })

@pytest.fixture
def population_df():
    return pd.DataFrame({
        'Nazwa': ['mazowieckie', 'małopolskie'],
        'ludność w tysiącach,2024,[tys. osób]': ['5000', '3000'],
        'ludność na 1 km2,2024,[osoba]': ['150', '120']
    })

@pytest.fixture
def pedestrian_df():
    return pd.DataFrame({
        'Wskaźnik: "Liczba wypadków drogowych z udziałem pieszych i rowerzystów na 100 tys. ludności"': [
            'mazowieckie;25',
            'małopolskie;20']
    })

def test_get_alcohol_concessions_number(alcohol_df):
    result = analysis.get_alcohol_concessions_number(alcohol_df)
    assert result['mazowieckie'] == 2
    assert result['małopolskie'] == 1

def test_get_fire_events_number(fire_df):
    result = analysis.get_fire_events_number(fire_df)
    assert result['mazowieckie'] == 25
    assert result['małopolskie'] == 5

def test_get_population_data(population_df):
    voivodeships = ['mazowieckie', 'małopolskie']
    pop, dens = analysis.get_population_data(population_df, voivodeships)
    assert pop.loc['mazowieckie'] == 5000.0
    assert dens.loc['małopolskie'] == 120.0

def test_get_pedestrian_data(pedestrian_df):
    voivodeships = ['mazowieckie', 'małopolskie']
    result = analysis.get_pedestrian_data(pedestrian_df, voivodeships)
    assert result['mazowieckie'] == '25'
    assert result['małopolskie'] == '20'

def test_fire_alcohol_correlation(fire_df, alcohol_df):
    r = analysis.fire_alcohol(fire_df, alcohol_df)
    assert -1 <= r <= 1

def test_fire_population_correlation(fire_df, population_df):
    r_pop, r_dens = analysis.fire_population(fire_df, population_df)
    assert -1 <= r_pop <= 1
    assert -1 <= r_dens <= 1

def test_alcohol_population_correlation(alcohol_df, population_df):
    r_pop, r_dens = analysis.alcohol_population(alcohol_df, population_df)
    assert -1 <= r_pop <= 1
    assert -1 <= r_dens <= 1
