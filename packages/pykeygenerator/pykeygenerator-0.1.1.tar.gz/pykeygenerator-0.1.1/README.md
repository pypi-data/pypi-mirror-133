# Pykeygen
A key generator made in python

## Installation 
`pip install pykeygenerator`

## Usage

To generate a key use the function `generate_key()`

### Example
```Python
import pykeygen as key
key.generate_key(length=10,include_letters=True,split=True,split_char="-",split_every=5)
```
Output:

**Note**: Output will be different each run

`9ZG9B-3890k-181AM-zGn78-Ofc7E-3j1XO-e2b6i-B516G-mg9m4-Chg4H-47r85-49P72-04PW4-wFh52-J1hd2-2qNs3-U3MuA-9C7SN-MJ6o9-e5IZM`

### Varibles in function

- length (Int): Defines how long the key is

- include_letters (Bool): Defines if to include letters into the key

- split (Bool): Defines if to include separators in the key e.g `0000-0000` e.g without `00000000`

- split_char (Str): Defines what to split the key with

- split_every (Int): Defines how many characters per split e.g split_every = 2 `00-00` split_every = 5 `00000-00000` 