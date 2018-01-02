Kumoricon Test Data Generator
===============================

Generates mock data for testing attendee import file
For information on the file format, see https://github.com/jashort/kumoreg/blob/master/docs/PreRegDataImportFormat.md

Requirements
---------------
Python 3
Faker.py 1.0


Usage 
---------------

```
python3 src/gen.py <number of rows>
```

Example:
```
python3 src/gen.py 5000 > ~/test.json
```

