## OceanBase Consistency Check Tool

Data Consistency check tool between two OB clusters.

- Supported list:
    * OceanBase <-> OceanBase
    * MySQL <-> OB
    * MySQL <-> MySQL

### Usage

#### Requirements
- dbutils
- loguru
- mysql-connector-python
- protobuf

```bash
git clone https://github.com/zetatez/obcc.git && cd obcc && pip install -r requirements.txt
```

#### Configuration
- config.py
- create database for diff
    ```sql
    create database diff;
    ```
#### To Run Script
    ```bash
    python obcc.py
    ```
