import pandas as pd
from pandas import DataFrame
from pandas.io.parsers import TextFileReader
import re


class Proc:

    @staticmethod
    def clean_non_important_inplace(data: DataFrame | TextFileReader) -> None:
        data.drop(columns=['country_code', 'university_rank', 'city', 'program_url'], inplace=True)
        data.dropna(subset=['country_name', 'program_name', 'duration'], inplace=True)

    @staticmethod
    def clean_program_inplace(data: DataFrame | TextFileReader) -> None:
        data.dropna(subset=['program_name', 'program_type'], inplace=True)

    @staticmethod
    def clean_ielts_scores_inplace(dataset: DataFrame | TextFileReader) -> None:
        max_ielts_score = dataset['ielts_score'].max()
        dataset['ielts_score'] = pd.to_numeric(dataset['ielts_score'], errors='coerce')
        dataset['ielts_score'].fillna(max_ielts_score, inplace=True)
        dataset.loc[dataset['ielts_score'] < 0, 'ielts_score'] = max_ielts_score
        dataset.loc[dataset['ielts_score'] > 9, 'ielts_score'] = max_ielts_score

    @staticmethod
    def clean_duration_inplace(data: DataFrame | TextFileReader) -> None:
        data['duration'] = data['duration'].str.extract(r'(\d+)')
        data.dropna(subset=['duration'], inplace=True)

    @staticmethod
    def clean_duration_inplace(data: DataFrame | TextFileReader) -> None:
        # Replace 'x months' or 'x month' values with the numeric part extracted
        data['duration'] = data['duration'].astype(str).str.replace(r'(\d+)\s+(months|month)', r'\1', regex=True)

        # Replace 'x days' or 'x day' values with the numeric part divided by 30
        data['duration'] = data['duration'].astype(str).str.replace(
            r'(\d+)\s+(days|day)',
            lambda m: str(int(m.group(1)) // 30),
            regex=True)

        # Remove any rows with null 'duration' values
        data.dropna(subset=['duration'], inplace=True)

        # Remove any rows where the duration is less than 3
        data['duration'] = data['duration'].astype(int)
        data.drop(data[data['duration'] < 3].index, inplace=True)
