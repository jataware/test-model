# Test Model

This repo is for model testing. It provides a test model for testing Dojo's model registration workflow.

## Usage

Install with `pip install -r requirements.txt`.

Next, edit the rainfall setting in `parameters.json` to a `float` between -1 and 1 (e.g. `0.7`), where 0 is no percentage perturbation to rainfall (baseline).
Next, edit the color_hue setting in `fakeDataType.json` to a `str` that is one of the following colors:"blue","red","yellow","green","purple","orange".

Then run with `python3 main.py --temp 1.2` where the value passed to `--temp` is the percentage perturbation to temperature (0 is baseline).

Outputs are stored to `output/output_{{ rainfall }}_{{ temp }}.csv` (based on the model parameters). For example, `output/output_0.7_1.2.csv`.

Now, this model also produces an Excel file, Geotiff, and NetCDF. The Geotiff and NetCDF files are based on an interpolated grid.

## Using Docker

```
docker build -t test-model .
```

then set `parameters.json` with the value of your choosing and run:

```
mkdir output
docker run -v $PWD/configFiles:/model/configFiles -v $PWD/output:/model/output --entrypoint python3 test-model  /model/main.py --temp=0.5
```
