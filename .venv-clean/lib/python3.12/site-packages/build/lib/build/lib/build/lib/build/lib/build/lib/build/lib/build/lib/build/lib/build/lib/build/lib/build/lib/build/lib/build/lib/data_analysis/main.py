import argparse
import pandas as pd
#import data_analysis.analysis as analysis
import analysis

def main(cli_args=None):
    parser = argparse.ArgumentParser('Argparser for data anaylysis')
    parser.add_argument("--fire_dataset", nargs="?", default="data/3.csv", help="dataset of fire events, in csv format", type=str)
    parser.add_argument("--fire_column_start", nargs="?", default=4, help="Number of starting column from which we can calculate statistics for the fire dataset", type=int)
    parser.add_argument("--alcohol_dataset", nargs="?", default="data/raport_zezwoleń_alkoholowych_czynych_na_dzień_4_lutego_2025_r..csv", help="dataset about alcohol consession", type=str)
    parser.add_argument("--area_dataset", nargs="?", default="data/Wykaz_powierzchni_wg_stanu_na_01012025_ha_km2.xlsx", help="dataset about alcohol consession", type=str)
    args = parser.parse_args()

    fire_dataset = analysis.load_data(args.fire_dataset)
    analysis.summarize_dataframe(fire_dataset, args.fire_column_start)

    alcohol_dataset = analysis.load_data(args.alcohol_dataset)
    area_dataset = analysis.load_data(args.area_dataset)

    r_value = analysis.fire_alcohol(fire_dataset, alcohol_dataset, plot=False)
    print(f"Wartość korelacji między liczbą pożarów a liczbą firm z koncecją alkoholu w województwach wynosi{round(r_value, 2)}")

    #moje właśne - większa gęstość ludności sprzyja więszej ilości pozarow Nazwa jednostki POLSKA, nazwa wojewodztwa i wypisane - wielkosci


if __name__ == "__main__":

    main()



