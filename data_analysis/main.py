import argparse
from data_analysis import analysis


def main(cli_args=None):
    parser = argparse.ArgumentParser('Argparser for data anaylysis')
    parser.add_argument("--fire_dataset", nargs="?", default="data/3.csv",
                        help="dataset of fire events, in csv format", type=str)
    parser.add_argument("--fire_column_start", nargs="?", default=4,
                        help="Number of starting column from which we can calculate statistics for the fire dataset", type=int)
    parser.add_argument("--alcohol_dataset", nargs="?", default="data/raport_zezwoleń_alkoholowych_czynych_na_dzień_4_lutego_2025_r..csv",
                        help="dataset about alcohol consession", type=str)
    parser.add_argument("--population_dataset", nargs="?",
                        default="data/LUDN_2425_CTAB_20250611231708.csv", help="dataset of population density", type=str)
    parser.add_argument("--pedestrian_accidents_dataset", nargs="?",
                        default="data/liczba_wypadkow.csv", help="dataset of population density", type=str)
    parser.add_argument("--output_file", default="wyniki_analizy.txt",
                        help="file to save output", type=str)
    parser.add_argument("--plot", default=1, type=int,
                        help="Parameter to set plotting, 0/1 (false/true)")

    args = parser.parse_args(cli_args)

    fire_dataset = analysis.load_data(args.fire_dataset)
    analysis.summarize_dataframe(fire_dataset, args.fire_column_start)

    alcohol_dataset = analysis.load_data(args.alcohol_dataset)
    population_dataset = analysis.load_data(args.population_dataset)
    pedestrian_accidents_dataset = analysis.load_data(
        args.pedestrian_accidents_dataset)

    print('Parsed data:')
    print(
        f'  Fire dataset filename: {args.fire_dataset}, shape: {fire_dataset.shape}')
    print(
        f'  Alcohol dataset filename: {args.alcohol_dataset}, shape: {alcohol_dataset.shape}')
    print(
        f'  Population dataset filename: {args.population_dataset}, shape: {population_dataset.shape}')
    print(
        f'  Pedestrian accidents dataset filename: {args.pedestrian_accidents_dataset}, shape: {pedestrian_accidents_dataset.shape}')
    print(f'  Plotting enabled: {bool(args.plot)}')
    print(f'  Fire column start index: {args.fire_column_start}')
    print(f'  Output will be saved to: {args.output_file}')

    # liczba pozarow a liczba koncesji
    with open(args.output_file, "w", encoding="utf-8") as f:
        r_value = analysis.fire_alcohol(
            fire_dataset, alcohol_dataset, plot=bool(args.plot))
        f.write(
            f"Wartość korelacji między liczbą pożarów a liczbą firm z koncecją alkoholu w województwach wynosi {round(r_value, 2)}. \n")

        # liczba ludnosci a liczba pozarow
        r_pop, r_den = analysis.fire_population(
            fire_dataset, population_dataset, plot=bool(args.plot))
        f.write(
            f"Wartość korelacji między liczbą pożarów a liczbą ludności w województwach wynosi {round(r_pop, 2)}. \n")
        f.write(
            f"Wartość korelacji między liczbą pożarów a gęstością ludności w województwach wynosi {round(r_den, 2)}. \n")

        # liczba ludnosci a liczba koncesji
        r_pop, r_den = analysis.alcohol_population(
            alcohol_dataset, population_dataset, plot=bool(args.plot))
        f.write(
            f"Wartość korelacji między liczbą koncesji a liczbą ludności w województwach wynosi {round(r_pop, 2)}. \n")
        f.write(
            f"Wartość korelacji między liczbą koncesji a gęstością ludności w województwach wynosi {round(r_den, 2)}. \n")

        # my own statistic - liczba wypadkow na 100 tys vs liczba koncesji/ liczbe ludnosci
        r = analysis.alcohol_pedestrian(
            alcohol_dataset, population_dataset, pedestrian_accidents_dataset, plot=bool(args.plot))
        f.write(
            f"Wartość korelacji między liczbą koncesji na liczbę ludności a liczbą wypadków z udziałem pieszych na 100 tys ludnosci w województwach wynosi {round(r, 2)}. \n")


if __name__ == "__main__":

    main()
