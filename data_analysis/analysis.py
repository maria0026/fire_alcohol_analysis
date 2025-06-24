import pandas as pd
import scipy
import matplotlib.pyplot as plt

def load_data(path: str) -> pd.DataFrame:
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


def get_alcohol_concessions_number(df_alcohol: pd.DataFrame):
    df_alcohol_voivodeships_grouped = df_alcohol.groupby('Województwo').count() #zliczenie ile razy pojawia się konkretne wojewodztwo
    alcohol_voivodeships_values = df_alcohol_voivodeships_grouped['Numer zezwolenia']

    return alcohol_voivodeships_values

def get_fire_events_number(df_fire: pd.DataFrame):
    df_fire_voivodeships_grouped = df_fire.groupby('Województwo').sum()
    fire_voivodeships_values = df_fire_voivodeships_grouped['OGÓŁEM Liczba zdarzeń']

    return fire_voivodeships_values

#either fire or alcohol dataset, which contains recognizable voivodeship names
def get_voivodeships_names(df: pd.DataFrame):
    df['Województwo'] = df['Województwo'].str.replace('WOJ. ', '').str.lower()
    voivodeship_names = df['Województwo']

    return voivodeship_names

def get_population_data(df_population: pd.DataFrame, voivodeship_names):
    df_population['Nazwa']= df_population['Nazwa'].str.lower() #wojewodztwa oryginalnie z wilkiej

    df_population_filtered = df_population[df_population['Nazwa'].isin(voivodeship_names)] #wybór tylko wierszy z wojewodztwami

    population = df_population_filtered['ludność w tysiącach,2024,[tys. osób]'].astype(float)
    density = df_population_filtered['ludność na 1 km2,2024,[osoba]'].astype(float)

    population.index = df_population_filtered['Nazwa']
    density.index = df_population_filtered['Nazwa']

    return population, density

def get_pedestrian_data(df: pd.DataFrame, voivodeship_names):
    df.columns = df.columns.str.strip().str.rstrip(';')
    df[['Województwo', 'Wartość']] = df[
    'Wskaźnik: "Liczba wypadków drogowych z udziałem pieszych i rowerzystów na 100 tys. ludności"'
    ].str.split(';', expand=True)
    df['Województwo'] = (df['Województwo'].str.lower()).str.strip()
    df_pedestrian_filtered = df[df['Województwo'].isin(voivodeship_names)] #wybór tylko wierszy z wojewodztwami
    pedestrian_values = df_pedestrian_filtered['Wartość']
    pedestrian_values.index= df_pedestrian_filtered['Województwo']

    return pedestrian_values


def fire_alcohol(df_fire: pd.DataFrame, df_alcohol: pd.DataFrame, plot=False) -> float:
    fire_voivodeships_values = get_fire_events_number(df_fire)
    alcohol_voivodeships_values = get_alcohol_concessions_number(df_alcohol)
    r, _ = scipy.stats.pearsonr(fire_voivodeships_values, alcohol_voivodeships_values)

    if plot:
        plt.scatter(fire_voivodeships_values, alcohol_voivodeships_values)
        plt.xlabel("Number of fire events in voivodeships")
        plt.ylabel("Number of alcohol selling concessions in voivodeships")
        plt.show()

    return r

def fire_population(df_fire: pd.DataFrame, df_population: pd.DataFrame, plot=False) -> float:
    voivodeship_names = get_voivodeships_names(df_fire)
    population, density = get_population_data(df_population, voivodeship_names)
    fire_voivodeships_values = get_fire_events_number(df_fire)
    fire_voivodeships_values = fire_voivodeships_values.reindex(population.index)

    r_pop, _ = scipy.stats.pearsonr(fire_voivodeships_values, population)
    r_den, _ = scipy.stats.pearsonr(fire_voivodeships_values, density)


    if plot:
        plt.figure()
        plt.scatter(fire_voivodeships_values, population)
        plt.xlabel("Number of fire events in voivodeships")
        plt.ylabel("Number of population [thousand]")
        plt.show()

        plt.figure()
        plt.scatter(fire_voivodeships_values, density)
        plt.xlabel("Number of fire events in voivodeships")
        plt.ylabel("Population density (nr of people/1 km^2)")
        plt.show()

    return r_pop, r_den


def alcohol_population(df_alcohol: pd.DataFrame, df_population: pd.DataFrame, plot = False):
    voivodeship_names = get_voivodeships_names(df_alcohol)
    population, density = get_population_data(df_population, voivodeship_names)

    alcohol_voivodeships_values = get_alcohol_concessions_number(df_alcohol)
    alcohol_voivodeships_values = alcohol_voivodeships_values.reindex(population.index)

    r_pop, _ = scipy.stats.pearsonr(alcohol_voivodeships_values, population)
    r_den, _ = scipy.stats.pearsonr(alcohol_voivodeships_values, density)

    if plot:
        plt.figure()
        plt.scatter(alcohol_voivodeships_values, population)
        plt.xlabel("Number of alcohol concessions in voivodeships")
        plt.ylabel("Number of population [thousand]")
        plt.show()

        plt.figure()
        plt.scatter(alcohol_voivodeships_values, density)
        plt.xlabel("Number of alcohol concessions in voivodeships")
        plt.ylabel("Population density (nr of people/1 km^2)")
        plt.show()

    return r_pop, r_den

def alcohol_pedestrian(df_alcohol: pd.DataFrame, df_population: pd.DataFrame, df_pedestrian: pd.DataFrame, plot = False):
    voivodeship_names = get_voivodeships_names(df_alcohol)
    alcohol_voivodeships_values = get_alcohol_concessions_number(df_alcohol)
    population, _ = get_population_data(df_population, voivodeship_names)
    alcohol_voivodeships_values = alcohol_voivodeships_values.reindex(population.index)

    pedestrian_values = get_pedestrian_data(df_pedestrian, voivodeship_names)
    pedestrian_values = pedestrian_values.reindex(population.index)

    alcohol_ratio = (alcohol_voivodeships_values / population).astype(float)
    pedestrian_values = pedestrian_values.str.replace(',', '.').astype(float)
    
    r, _ = scipy.stats.pearsonr(alcohol_ratio, pedestrian_values)

    if plot:
        plt.figure()
        plt.scatter(alcohol_ratio, pedestrian_values)
        plt.xlabel("Number of alcohol concessions/number of population [thousand]")
        plt.ylabel("Pedestrian accidents number")
        plt.show()

    return r

