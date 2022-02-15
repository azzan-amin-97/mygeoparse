
## mygeoparse
![GitHub](https://img.shields.io/github/license/azzan-amin-97/mygeoparse)

Address Parser for Malaysian Address 

### Installation
Requirement Python >= 3.6
* install from PyPI
```shell
pip install mygeoparse
```


### Usage:

```python
# setup
from mygeoparse import MalaysianAddressParser
```

#### Parse One Address:

```python
# import class from module
from mygeoparse import MalaysianAddressParser

# create object Parser
myAddressParser = MalaysianAddressParser()

# Parsing one Address
result = myAddressParser.parser("1-6-6, Icon Residenz, Jalan SS 8/2, Sungei Way, 47300 Petaling Jaya")

print(result)

```

#### Parse List of Addresses:
```python
# Parsing List of Addresses
result = myAddressParser.parser(
    ["1-6-6, Icon Residenz, Jalan SS 8/2, Sungei Way, 47300 Petaling Jaya",
     "A-1-2, Riana Green Condominium, Jalan Tropicana Utara, PJU 3, 47410, Petaling Jaya, Selangor"]
)

print(result)
```

## Copyright
Copyright (c) 2022 Azzan Amin. Released under the MIT License. 

Third-party copyright in this distribution is noted where applicable.

### Reference
* [Github Project](https://github.com/azzan-amin-97/tlo-my-address-parser)