# Test Model

This repo is for model testing with more parameters. It provides a slightly more complex test model for testing Dojo's model registration workflow.

## Usage

Install with `pip install -r requirements.txt`.

Next, edit the rainfall setting in `parameters.json` to a `float` between -1 and 1 (e.g. `0.7`), where 0 is no percentage perturbation to rainfall (baseline).
Next, edit the score setting in `parameters.json` to an `float` where between 0 and 1.

Next, edit the face setting in `parameters.json` to a `str` that is one of the strings:":)",":|",":(",">:(",":()".

Next, edit the color_hue setting in `fakeDataType.json` to a `str` that is one of the following colors:"blue","red","yellow","green","purple","orange".

Next, edit the magic_bumber setting in `fakeDataType.json` to an `int` which will be the output name.


Then run with `python3 main.py --temp 1.2 --space 1` where the value passed to `--temp` is the percentage perturbation to temperature (0 is baseline)
and `--space` is the number of spaces between face and score.

Outputs are stored to `output/output_{{ rainfall }}_{{ temp }}.csv` and `{{ magic_number.txt}}` (based on the model parameters). 
For example, `output/output_0.7_1.2.csv` and `128.txt`. (The `.txt` should be tagged as media for Dojo even though it is output.
Simulates a slightly different scenario to perfectly split media and output.)

## Using Docker

```
docker build -t dummy-model .
```

then, from an empty directory (not the project base), where you have a copy of `parameters.json` filled with the value of your choosing, run:

```
docker run -v $PWD/configFiles:/model/configFiles -v $PWD:/model/output --entrypoint python3 dummy-model  /model/main.py --temp=0.5
```
