import pandas as pd
import  numpy as np

if __name__ == '__main__':
    dataArr = pd.read_csv("../Files/201709301651_masters_portal.csv")
    print(dataArr)
    df = pd.DataFrame(dataArr)
    dataArr = df.drop(columns=['country_code', 'university_rank', 'city', 'program_url'])
    print(dataArr)
    df = pd.DataFrame(dataArr)
    dataArr = df[df.tution_2_money.notnull() & df.program_name.notnull()]
    print(dataArr)


