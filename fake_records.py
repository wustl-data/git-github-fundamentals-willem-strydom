

from faker import Faker
import pandas as pd
import numpy as np

fake = Faker()


def generate():
    namesf = [fake.name() for i in range(1000)]
    namesl = [fake.last_name() for i in range(1000)]
    bday = [fake.birthday() for i in range(1000)]
    email = [fake.email() for i in range(1000)]
    pnum = [fake.phone_number() for i in range(1000)]
    df = pd.DataFrame({'First Name': namesf, 'Last Names': namesl, 'Birthday': bday, 'Email': email,
                       'Phone Number': pnum})
    return df
def save():
    df = generate()
    file_path = "desktop/cse314/git-github-fundamentals-willem-strydom/.github/data"
    with open(file_path, 'w', newline='') as file:
        df.to_csv("fake_records.csv", index=False)

def assign_salaries(df):
    salaries = [np.random.randint(20000,100000) for i in range(1000)]
    df = df.assign(Salary = salaries)
    return df

def over_50k(df):
    df = df[df['Salary']>50000]
    return df

def normalize(series):
    return (series - series.mean()) / series.std()

def assign_normalized_salaries(df):
    df = df.assign(Normalized_Salaries = normalize(df['Salary']))
    return df
