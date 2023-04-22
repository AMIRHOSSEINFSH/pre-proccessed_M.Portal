import re
import pandas as pd
import numpy as np
from proc import Proc as p
from datetime import datetime

if __name__ == '__main__':
    dataArr = pd.read_csv("../Files/201709301651_masters_portal.csv")
    # dataArr.info()
    # print(dataArr['deadline'].unique())
    # dataArr.head()
    p.preprocess(dataArr)

    # print(dataArr['tuition_price_specification'].unique())

    # Save the cleaned dataset to the same CSV file
    dataArr.to_csv('../Files/output.csv', index=True)
    # print(dataArr)
