# Betterjson
[Library](https://github.com/DarkJoij/betterjsondb) for easier working with JSON files in Python.

# Quick example
```json
{"names": ["Alex", "Allan"]}
```
```py
import betterjsondb

db = betterjsondb.connect(file="tests.json", prefix="~")                  # Name of file and prefix can be custom

print(                                                                    # In concole you'll see:
    db.get("all"),                                                        # {'names': ['Alex', 'Allan']}
    db.push("cars", {"BMW": "car", "Tosiba": "not_car"}, callback=True),  # True
    db.update("cars", "=", {"BMW": "car"}, callback=True),                # True
    db.delete("names", callback=True),                                    # True
    db.get("all")                                                         # {'cars': {'BMW': 'car'}}
)
```

# Important information
27.12.2021 library updated using [Python 3.10](https://www.python.org/downloads/release/python-3100/). So now its strictly requere it on your PC.

# Changelog:
#### v. 0.1.8:

After connect file if its not exists library will create it.
Added warning to not existing file.
