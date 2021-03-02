import sys
import random
import json
import pandas as pd
from faker import Faker
from collections import OrderedDict
import urllib.request

if __name__ == "__main__":
    outfile = sys.argv[1]
    params = open('parameters.json').read()
    params = json.loads(params)


    print('Beginning to download file from S3...')

    url = 'https://jataware-world-modelers.s3.amazonaws.com/dummy-model/input.csv'
    urllib.request.urlretrieve(url, 'input.csv')


    locales = OrderedDict([
        ('en-US', 1)
    ])
    fake = Faker(locales)
    f = fake['en_US']    
    data = []

    for i in range(100):
        obj = dict(latitude=f.latitude(),
                   longitude=f.longitude(),
                   date=f.date(),
                   value=random.random()*params['rainfall'])
        data.append(obj)

    df = pd.DataFrame(data)
    print(df.head())
    df.to_csv(outfile,index=False)