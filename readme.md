# Get dataset

## How to get dataset

### MUST DO

1. You must have credentials.json file
2. If it prompt you to login, You **must** use @student.tu.ac.th to access API
3. Create *directory* `credential` and put credentials.json init
4. Download Data collection `.csv` **(Don't rename it)** and put it in the same level as get_file.py
   1. File structure look like this
      - get_file.py
      - Data Collection.csv **(Don't rename it)**
      - credential
        - |
        - -- credentials.json

### How to run

I highly suggest you to run this in virtual environtment

`python -m venv .venv` followed by `source .venv/Scripts/activate` or `source .venv/bin/activate`

Install requirements

`pip install -r requirements.txt`

If you do everything correctly just type `python get_file.py` or `python3 get_file.py` (linux)
