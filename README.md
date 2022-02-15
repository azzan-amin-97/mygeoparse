
## tlo-my-address-parser
[![Build Status](https://travis-ci.org/jingw2/size_constrained_clustering.svg?branch=master)](https://travis-ci.org/jingw2/size_constrained_clustering)
[![PyPI version](https://badge.fury.io/py/size-constrained-clustering.svg)](https://badge.fury.io/py/size-constrained-clustering)
![GitHub](https://img.shields.io/github/license/jingw2/size_constrained_clustering)
[![codecov](https://codecov.io/gh/jingw2/size_constrained_clustering/branch/master/graph/badge.svg)](https://codecov.io/gh/jingw2/size_constrained_clustering)
![PyPI - Downloads](https://img.shields.io/pypi/dm/size-constrained-clustering)
![Codecov](https://img.shields.io/codecov/c/github/jingw2/size_constrained_clustering)


Address Parser for Malaysian Address 

### Installation
Requirement Python >= 3.6
* install from PyPI
```shell
pip install tlo-my-address-parser
```

### Methods
* My Module algorithms


### Usage:
```python
# setup
from tlo_my_address_parser import MalaysianAddressParser
```

#### Parse One Address:
```python
# import class from module
from tlo_my_address_parser import MalaysianAddressParser

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
* [Github Project](https://github.com/tribasuki74/myenglish)