import re
import pandas as pd
import numpy as np
from proc import Proc as p

if __name__ == '__main__':
    dataArr = pd.read_csv("../Files/201709301651_masters_portal.csv")
    dataArr.head()
    p.clean_non_important_inplace(dataArr)
    p.clean_program_inplace(dataArr)
    p.clean_ielts_scores_inplace(dataArr)
    p.clean_duration_inplace(dataArr)
    p.clean_duration_inplace(dataArr)

    # Save the cleaned dataset to the same CSV file
    dataArr.to_csv('../Files/output.csv', index=True)
    # print(dataArr)
