import re
import pandas as pd
import numpy as np
from proc import Proc as p
from datetime import datetime
from seleniumStuff import Sel
from time import sleep

if __name__ == '__main__':
    # dataArr = pd.read_csv("../Files/201709301651_masters_portal.csv")
    # p.preprocess(dataArr)
    # dataArr.to_csv('../Files/output.csv', index=True)

    university_name  = input("Enter the university name: ")

    program_name = input("Enter the program name: ")

    optional_keywords = input("Enter any optional keywords seperated with comma(press enter to skip): ")

    dataArr2 = pd.read_csv("../Files/output.csv")

    Sel.start(university_name, program_name, optional_keywords.split(",") + (dataArr2.loc[0, 'structure'])[1:-1].split(","))
