from settings import BASE_TEMP

def calculate_gdd_series(df):

    cumulative = 0
    cumulative_list = []

    for _, row in df.iterrows():

        temp = row["temperature"]   # Use temperature from forecast

        gdd = max(0, temp - BASE_TEMP)

        cumulative += gdd
        cumulative_list.append(cumulative)

    df["cumulative_gdd"] = cumulative_list

    return df
