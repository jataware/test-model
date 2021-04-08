# Dummy Model

This repo is for model testing. It provides a test dummy model.

## Usage

Install with `pip -r requirements.txt`.

Next, edit the rainfall setting in `parameters.json` to a `float` between -1 and 1 (e.g. `0.7`), where 0 is no percentage perturbation to rainfall (baseline).

Then run with `python3 main.py --temp 1.2` where the value passed to `--temp` is the percentage perturbation to temperature (0 is baseline).

Outputs are stored to `output/output_{{ rainfall }}_{{ temp }}.csv` (based on the model parameters). For example, `output/output_0.7_1.2.csv`.

## Using Docker

```
docker build -t dummy-model .
```

then, from an empty directory (not the project base), where you have a copy of `parameters.json` filled with the value of your choosing, run:

```
docker run -v $PWD/parameters.json:/model/parameters.json -v $PWD:/model/output dummy-model --temp=0.9
```