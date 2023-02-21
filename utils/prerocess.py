from datetime import date

import pandas as pd


def read_stock_df(dataset_path, start_date=None, end_date=None, drops_columns=None, missing_date=True):
    date_column_name = 'Date'

    df = pd.read_csv(dataset_path, date_parser=True)

    if drops_columns:
        df = df.drop(drops_columns, axis=1)
    df[date_column_name] = pd.to_datetime(df[date_column_name], utc=True)
    df[date_column_name] = df[date_column_name].dt.date

    # 特定年份資料提取
    if start_date and end_date:
        df = df[df[date_column_name] >= date.fromisoformat(start_date)]
        df = df[df[date_column_name] < date.fromisoformat(end_date)]
    else:
        start_date = start_date if start_date else df.Date.min()
        end_date = end_date if end_date else df.Date.max()

    # 將不是交易日的資料填充為NaN，避免套件的時間特徵出錯
    if missing_date:
        missing_date = pd.date_range(start=start_date, end=end_date).difference(df[date_column_name])

        df_missing = pd.DataFrame(missing_date, columns=[date_column_name])
        df_missing[date_column_name] = df_missing[date_column_name].dt.date

        df_full = pd.concat([df, df_missing])
        df_full = df_full.sort_values(by=[date_column_name])

        df = df_full.reset_index(drop=True)
        # df = df_full.set_index(date_column_name)

    return df
