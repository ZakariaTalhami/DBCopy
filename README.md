# DBCopy

## setup:
1. Clone the repository locally.

        git clone https://github.com/ZakariaTalhami/DBCopy.git

1. Create a python virtual environment.

        python -m venv <venv>

        # if python2 is the default python
        python3 -m venv <venv>

1. Activate the python virtual environment.

        # Linux or MacOS
        source <venv>/bin/activate

        # Windows
        <venv>\Scripts\activate.bat
    
1. Install the required packages.

        pip install -r requirements.txt


## Usage:

### How to configure the Databases:
In order to copy the tables from database to the other, the database configuration will need to be setup.

The default **from** and **to** database configurations are stored in `conf/settings.json`

```json
{
    "from_db": {
        "host": "",
        "port": "",
        "name": "",
        "username": "",
        "password": ""
    },
    "to_db": {
        "host": "",
        "port": "",
        "name": "",
        "username": "",
        "password": ""
    }
}
```
Fill in the values with the appropriate values for the given databases.

### How to Specify the database tables to be copied:

In `Conf/tables.json` the tables are specified.

```json
{
    "tables": [
        "<table1>",
        "<table2>",
        "<table3>"
    ]
}
```

Fill the `tables` array with the list of tables to be copied. The tables will be copied in order provide in the configuration, in the case of relations, the tables should be arrange in order of relation.

### Running the command:

To run the command:

```bash
python main.py
```

if there are some constriant issues, they can be skipped by appending the command with `-sc`

```
python main.py -sc
```


## Multiple Configurations
If there are more than one set of database that are frequently copied from, multiple configurations JSON files can be created, and then specifed in the command.

### Example:
Say there was two sets of databases [local-db, dev-db] and [local-db, prod-db], these sets can be configured into two JSON files:

1. `conf/local-dev-db.json`
1. `conf/local-prod-db.json`

Then each set can be used separatly with out the need to reconfigure eache time, this can be accumplished using: 

```
python main -c conf/local-dev-db.json
python main -c conf/local-prod-db.json
```

The same can be done with the tables configurtion:

```
python main -c conf/local-dev-db.json -t app1-tables.json
python main -c conf/local-dev-db.json -t app2-tables.json
```