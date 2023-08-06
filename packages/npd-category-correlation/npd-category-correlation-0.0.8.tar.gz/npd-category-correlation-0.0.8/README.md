# Introduction 
This package has been created for the purpose of integrating Bloomberg Data with NPD Equity Watch data.

# Installation
IMPORTANT: you must separately install the Bloomberg Python API before use (first line below)
```bash
python -m pip install --index-url=https://bcms.bloomberg.com/pip/simple blpapi

python -m pip install npd_cat_corr==0.0.8
```

# Use Case: Creating Category Correlation Dataset
The get-correlation-dataset command takes two parameters: the path to your local EW flat file (must be CSV readable) and your desired output path (if left blank will be directory in which you run the command)

```bash
get-correlation-dataset path/to/FlatFile/EW_DATA.gz path/to/output/correlation_data.csv
``` 


