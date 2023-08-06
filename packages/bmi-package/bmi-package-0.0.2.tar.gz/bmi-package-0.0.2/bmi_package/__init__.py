import json
import pandas as pd





def bmi_reports(row):
    """
    Objective : Find the value of BMI Category based on BMI value
    Input : series of dataframe with BMI value
    Output : Tuple ( BMI , BMI Category , Health Risk )

    """
    try:
        bmi = row['WeightKg'] / ((row['HeightCm'] / 100) ** 2)
        if bmi <= 18.4:
            return bmi, 'Underweight', 'Malnutrition Risk'
        elif 18.5 <= bmi <= 24.9:
            return bmi, 'Normal Weight', 'Low Risk'
        elif 25 <= bmi <= 29.9:
            return bmi, 'Overweight', 'Enhanced Risk'
        elif 30 <= bmi <= 34.9:
            return bmi, 'Moderately Obese', 'Medium Risk'
        elif 35 <= bmi <= 39.9:
            return bmi, 'Severely Obese', 'High Risk'
        elif 40 <= bmi:
            return bmi, 'Very Severely Obese', 'Very High Risk'

    except Exception as e:
        print(e)

def getUpdatedTable(filename):
    """
    Objective: Read raw data json and return the updated Table
    Input : Input JSON file name
    Output : Updated table in the form of dataframe

    """
    # Raw Data Read #
    with open(filename) as f:
        rawdata = json.load(f)
    # convert list of dictionary to a dataframe #
    df = pd.DataFrame(rawdata)
    # Adding BMI, BMI Category and Health Risk #
    df['BMI'] = df.apply(lambda row: bmi_reports(row)[0], axis=1)
    df['BMI Category'] = df.apply(lambda row: bmi_reports(row)[1], axis=1)
    df['Health Risk'] = df.apply(lambda row: bmi_reports(row)[2], axis=1)
    return df


def count_overweight(df):
    """
    Objective : This function basically returns the number of Overweight people
    Input :  Dataframe with BMI value
    Output : Total number of overweight people


    """
    try:
        if not df.empty:
            return len(df[df['BMI Category'] == 'Overweight'])
        else:
            return None
    except Exception as e:
        print(e)
