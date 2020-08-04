# wind-converter

# run tests
tox

# run application (python 3.8 preferred, may work with other versions)
python3 converter.py --help # usage
python3 converter.py --in sample.csv  --out results.csv
python3 converter.py --in sample.csv --average 10 --out results.csv

