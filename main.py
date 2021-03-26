import click
import random
import json
import pandas as pd
from faker import Faker
from collections import OrderedDict
import urllib.request

@click.command()
@click.option('--temp', type=float, default=1.0, help='Percentage perturbation to temperature.')
def main(temp):
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

    perturbation = 1 + (params['rainfall']*temp)
    for i in range(100):
        obj = dict(latitude=f.latitude(),
                   longitude=f.longitude(),
                   date=f.date(),
                   value=random.random()*perturbation)
        data.append(obj)

    df = pd.DataFrame(data)
    print(df.head())
    df.to_csv('output.csv', index=False)

if __name__ == "__main__":
    main()