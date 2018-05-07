import pandas as pd
import os
from ParsingZumi import ZumiParser

def iterate_directory(directory):
    merged_df = pd.DataFrame()
    i = 1
    for filename in os.listdir(directory):
        print(i)
        i += 1
        if filename.endswith(".csv"):
            new_dataframe = pd.read_csv(os.path.join(directory, filename),
                        delimiter=';')
            if not new_dataframe.empty:
                merged_df = pd.concat([merged_df, new_dataframe])
    merged_df.drop_duplicates(inplace=True, keep='first')
    print("Finished merging")
    merged_df.to_csv(directory+"FINALE1.csv", index=False, index_label=False, sep=';')
    return merged_df
if __name__ == "__main__":
    directory = "csv/csv1"
    merged_df = iterate_directory(directory)
    merged_df['nip'] = merged_df['nip'].str.replace('-', '')
    merged_df['nip'].dropna(inplace=True)

    merged_df['number'] = merged_df['nip'].apply(lambda x: ZumiParser.getNumber(ZumiParser.getTempAddres(x)))
    merged_df['email'] = merged_df['nip'].apply(lambda x: ZumiParser.getMail(ZumiParser.getTempAddres(x)))

    merged_df['number'] = merged_df['number'].str.replace('-', '')
    merged_df['email'] = merged_df['email'].str.replace('Aktualizuj adres e-mail', '')
    merged_df['number'] = merged_df['number'].str.replace('(', '')
    merged_df['number'] = merged_df['number'].str.replace(')', '')

    print(merged_df[['number', 'email']])
    merged_df.to_csv(directory+"FINALE3.csv", index=False, index_label=False, sep=';')
