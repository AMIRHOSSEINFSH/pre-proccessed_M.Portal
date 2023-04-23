import time

import pandas as pd
import re
import collections.abc
import pandas as pd
from pandas import DataFrame, Series
from pandas.io.parsers import TextFileReader
import re
import math
import numpy as np
from datetime import datetime, timedelta


class Proc:
    @staticmethod
    def extract_number(s: str) -> float:
        try:
            return float(re.findall(r'\d+\.*\d*', s)[0])
        except:
            return np.nan

    @staticmethod
    def __rename_columns_inplace(data: DataFrame) -> None:
        data.rename(columns={"tution_1_currency": "tuition_1_currency",
                             "tution_1_money": "tuition_1_money",
                             "tution_1_type": "tuition_1_type",

                             "tution_2_currency": "tuition_2_currency",
                             "tution_2_money": "tuition_2_money",
                             "tution_2_type": "tuition_2_type"}, inplace=True)

    @staticmethod
    def __clean_non_important_inplace(data: DataFrame) -> None:
        data.drop(columns=['country_code', 'university_rank', 'city', 'program_url'], inplace=True)
        data.dropna(subset=['country_name', 'program_name'], inplace=True)

    @staticmethod
    def __clean_program_inplace(data: DataFrame) -> None:
        data.dropna(subset=['program_name'], inplace=True)

    @staticmethod
    def __clean_ielts_scores_inplace(dataset: DataFrame) -> None:
        max_ielts_score = dataset['ielts_score'].max()
        dataset['ielts_score'] = pd.to_numeric(dataset['ielts_score'], errors='coerce')
        dataset['ielts_score'].fillna(max_ielts_score, inplace=True)
        dataset.loc[dataset['ielts_score'] < 0, 'ielts_score'] = max_ielts_score
        dataset.loc[dataset['ielts_score'] > 9, 'ielts_score'] = max_ielts_score

    @staticmethod
    def __clean_duration_inplace(data: DataFrame) -> None:
        # Drop any rows with null values in 'duration' column
        # data.dropna(subset=['duration'], inplace=True)

        # Drop any rows where 'duration' value doesn't match the expected format
        # data.drop(data[~data['duration'].astype(str).str.match(r'^\d+\s+(months|month|days|day)$')].index,
        #           inplace=True)

        # Replace 'x months' format with 'x' and convert column to int type
        data['duration'] = data['duration'].astype(str).str.replace(r'(\d+)\s+(months|month)', r'\1', regex=True)

        # Replace 'x days' format with 'x/30' and convert column to int type
        data['duration'] = data['duration'].astype(str).str.replace(r'(\d+)\s+(days|day)',
                                                                    lambda m: str(int(m.group(1)) // 30),
                                                                    regex=True)
        data['duration'] = pd.to_numeric(data['duration'], errors='coerce').fillna(-1)
        data['duration'] = data['duration'].astype(int)

        # Drop any rows where 'duration' value is less than 3 moths and more than 60 month (5 years)
        # data.drop(data[data['duration'] < 3].index, inplace=True)
        # data.drop(data[data['duration'] > 60].index, inplace=True)

    @staticmethod
    def __clean_tuition_inplace(data: DataFrame) -> None:

        def clean_tuition_semester(row: Series) -> None:
            # Calculate number of semesters by dividing duration by 6 and rounding up
            num_semesters = math.ceil(row['duration'] / 6)

            # Multiply tuition by number of semesters
            row['tuition_1_money'] *= num_semesters
            row['tuition_2_money'] *= num_semesters

        def clean_tuition_full_programme(row: Series) -> None:
            row['tuition_1_money'] = Proc.extract_number(row['tuition_1_money'])
            row['tuition_2_money'] = Proc.extract_number(row['tuition_2_money'])

        def clean_tuition_credit(row: Series) -> None:
            tuition_1_money = row['tuition_1_money']
            tuition_2_money = row['tuition_2_money']
            structure = row['structure']

            if not pd.isna(structure):
                num_structure = len(structure.split(','))
                if not pd.isna(tuition_1_money):
                    row['tuition_1_money'] = tuition_1_money * num_structure
                if not pd.isna(tuition_2_money):
                    row['tuition_2_money'] = tuition_2_money * num_structure

        def clean_tuition_nan(row: Series) -> None:
            row['tuition_1_money'] = Proc.extract_number(row['tuition_1_money'])
            row['tuition_2_money'] = Proc.extract_number(row['tuition_2_money'])

        def clean_tuition_module(row: Series) -> None:
            clean_tuition_credit(row)

        def clean_tuition_trimester(row: Series) -> None:
            # Calculate number of trimesters by dividing duration by 3 and rounding up
            num_trimesters = math.ceil(row['duration'] / 3)

            # Multiply tuition by number of years
            row['tuition_1_money'] *= num_trimesters
            row['tuition_2_money'] *= num_trimesters

        def clean_tuition_month(row: Series) -> None:
            # Calculate number of months by simply getting the duration because its unit is months
            num_months = row['duration']

            # Multiply tuition by number of months
            row['tuition_1_money'] *= num_months
            row['tuition_2_money'] *= num_months

        def clean_tuition_quarter(row: Series) -> None:
            # Calculate number of quarters by dividing duration by 3 and rounding up same as trimesters
            num_quarters = math.ceil(row['duration'] / 3)

            # Multiply tuition by number of quarters
            row['tuition_1_money'] *= num_quarters
            row['tuition_2_money'] *= num_quarters

        def clean_tuition_year(row: Series) -> None:
            # Calculate number of years by dividing duration by 12 and rounding up
            num_years = math.ceil(row['duration'] / 12)

            # Multiply tuition by number of years
            row['tuition_1_money'] *= num_years
            row['tuition_2_money'] *= num_years

        # Drop rows with null "tuition_1_money" and "tuition_price_specification" columns
        # data.dropna(subset=['tuition_1_money', 'tuition_price_specification'], inplace=True)

        # Create a dictionary to map "tuition_price_specification" values to cleaning functions
        cleaning_functions = {
            "Tuition (Year)": clean_tuition_year,
            "Tuition (Semester)": clean_tuition_semester,
            "Tuition (Full programme)": clean_tuition_full_programme,
            "Tuition (Credit)": clean_tuition_credit,
            np.nan: clean_tuition_nan,
            "Tuition (Module)": clean_tuition_module,
            "Tuition (Trimester)": clean_tuition_trimester,
            "Tuition (Month)": clean_tuition_month,
            "Tuition (Quarter)": clean_tuition_quarter
        }

        # filter rows where duration is not -1
        filtered_data = data[data['duration'] != -1]

        # apply the cleaning functions only to filtered rows
        filtered_data.apply(lambda row: cleaning_functions[row['tuition_price_specification']](row), axis=1)

        # update the original dataframe with the cleaned data
        data.update(filtered_data)

    @staticmethod
    def __clean_dates(data: DataFrame) -> None:

        data['deadline'] = pd.to_datetime(data['deadline'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')

        data['start_date'] = pd.to_datetime(data['start_date'], format=' %Y-%m-%d %H:%M:%S', errors='coerce')

        # Check if any of the dates are not valid and replace them with undefined datetime
        data['deadline'] = data['deadline'].apply(lambda x: pd.NaT if pd.isna(x) else x)
        data['start_date'] = data['start_date'].apply(lambda x: pd.NaT if pd.isna(x) else x)

        # Compare deadline and start_date columns and replace the deadline with one year before start_date if
        # deadline is after start_date
        mask = data['deadline'] > data['start_date']
        data.loc[mask, 'deadline'] = data.loc[mask, 'start_date'] - timedelta(days=365)

    @staticmethod
    def __clean_structures(data: DataFrame) -> None:

        array = data['structure']

        statementArrays = ["I have good knowledge in ", "I am interested in ",
                           "I have good grade at ", "I love to Continue in "]

        new_row = []
        for i, row in enumerate(array):
            newArray = []
            if type(row) is not float:
                for item in row.split(","):
                    item = re.sub(r"'", "", item)
                    item = re.sub(r"\[", "", item)
                    item = re.sub(r"\]", "", item)
                    item = re.sub(r'\([^()]*\)', '', item)
                    newArray.append(random.choice(statementArrays) + item)
            new_row.append(newArray)

        data['structure'] = new_row

    @staticmethod
    def preprocess(data: DataFrame) -> None:
        Proc.__rename_columns_inplace(data)
        Proc.__clean_non_important_inplace(data)
        Proc.__clean_program_inplace(data)
        Proc.__clean_ielts_scores_inplace(data)
        Proc.__clean_duration_inplace(data)
        Proc.__clean_tuition_inplace(data)
        Proc.__clean_dates(data)
        Proc.__clean_structures(data)
