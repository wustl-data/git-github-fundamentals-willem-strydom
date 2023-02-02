# Write a function generate in your new fake_records module that generates a DataFrame
# of 1000 records with the following
# fields: First Name, Last Name, Birthday, Email, and Phone Number

import Faker
import pandas as pd

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
