import pandas as pd
import scipy
import matplotlib.pyplot as plt

def load_data(path):
    if path.endswith(".csv"):
        dataset = pd.read_csv(path)
    elif path.endswith(".xlsx"):
        dataset = pd.read_excel(path)

    dataset = dataset.loc[:, ~dataset.columns.str.contains('Unnamed')]

    return dataset


def summarize_dataframe(df: pd.DataFrame, column_nr: int):
    desc=df.iloc[:, column_nr:].describe(include='all')
    desc.loc['sum'] = df.sum(numeric_only=True) #sum added
    print(desc)


def fire_alcohol(df_fire: pd.DataFrame, df_alcohol: pd.DataFrame, plot=False):
    df_fire_voivodeships_grouped = df_fire.groupby('Województwo').sum()
    fire_voivodeships_values = df_fire_voivodeships_grouped['OGÓŁEM Liczba zdarzeń']

    df_alcohol['Województwo'] = df_alcohol['Województwo'].str.replace('WOJ. ', '').str.lower()
    df_alcohol_voivodeships_grouped = df_alcohol.groupby('Województwo').count()
    alcohol_voivodeships_values = df_alcohol_voivodeships_grouped['Numer zezwolenia']

    r, _ = scipy.stats.pearsonr(fire_voivodeships_values, alcohol_voivodeships_values)

    if plot:
        plt.scatter(fire_voivodeships_values, alcohol_voivodeships_values)
        plt.xlabel("Number of fire events in voivodeships")
        plt.ylabel("Number of alcohol selling concessions in voivodeships")
        plt.show()

    return r

def fire_population(df_fire: pd.DataFrame, df_population: pd.DataFrame, plot=False):
    voivodeship_names = df_fire['Województwo']
    df_population['Nazwa']= df_population['Nazwa'].str.lower()

    df_population_filtered = df_population[df_population['Nazwa'].isin(voivodeship_names)] #chose only voivodeship rows

    population=df_population_filtered['ludność w tysiącach,2024,[tys. osób]']
    density = df_population_filtered['ludność na 1 km2,2024,[osoba]']

    df_fire_voivodeships_grouped = df_fire.groupby('Województwo').sum()
    fire_voivodeships_values = df_fire_voivodeships_grouped['OGÓŁEM Liczba zdarzeń']

    r_pop, _ = scipy.stats.pearsonr(fire_voivodeships_values, population)
    r_den, _ = scipy.stats.pearsonr(fire_voivodeships_values, density)

    if plot:
        plt.scatter(fire_voivodeships_values, population)
        plt.xlabel("Number of fire events in voivodeships")
        plt.ylabel("Number of population [thousand]")
        plt.show()

        plt.scatter(fire_voivodeships_values, population)
        plt.xlabel("Number of fire events in voivodeships")
        plt.ylabel("Population density (nr of people/1 km^2)")
        plt.show()

    return r_pop, r_den


def alcohol_population(df_alcohol: pd.DataFrame, df_population: pd.DataFrame, plot = False):

    df_alcohol['Województwo'] = df_alcohol['Województwo'].str.replace('WOJ. ', '').str.lower()
    voivodeship_names = df_alcohol['Województwo']

    df_population['Nazwa']= df_population['Nazwa'].str.lower()

    df_population_filtered = df_population[df_population['Nazwa'].isin(voivodeship_names)] #chose only voivodeship rows

    population=df_population_filtered['ludność w tysiącach,2024,[tys. osób]']
    density = df_population_filtered['ludność na 1 km2,2024,[osoba]']

    df_alcohol_voivodeships_grouped = df_alcohol.groupby('Województwo').count()
    alcohol_voivodeships_values = df_alcohol_voivodeships_grouped['Numer zezwolenia']

    r_pop, _ = scipy.stats.pearsonr(alcohol_voivodeships_values, population)
    r_den, _ = scipy.stats.pearsonr(alcohol_voivodeships_values, density)

    if plot:
        plt.scatter(alcohol_voivodeships_values, population)
        plt.xlabel("Number of alcohol concessions in voivodeships")
        plt.ylabel("Number of population [thousand]")
        plt.show()

        plt.scatter(alcohol_voivodeships_values, population)
        plt.xlabel("Number of alcohol concession in voivodeships")
        plt.ylabel("Population density (nr of people/1 km^2)")
        plt.show()

    return r_pop, r_den


