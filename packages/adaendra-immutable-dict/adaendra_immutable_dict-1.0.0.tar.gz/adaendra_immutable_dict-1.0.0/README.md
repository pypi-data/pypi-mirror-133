# Python Immutable Dict

![badge](https://img.shields.io/badge/version-1.0.0-blue)

This library contains the **ImmutableDict**, a Python dictionary which can't be updated.

## How to use it
1. Install it from [**pip**](https://pypi.org/project/adaendra-immutable-dict/)
> pip install adaendra-immutable-dict
2. Import the **AdaendreImmutableDict**
> from adaendra_immutable_dict.AdaendraImmutableDict import AdaendraImmutableDict
3. Use it like in the following examples.

### Examples
```python
from adaendra_immutable_dict.AdaendraImmutableDict import AdaendraImmutableDict

# Empty Immutable Dict
immutable_dict = AdaendraImmutableDict({})

# Non empty Immutable Dict
immutable_dict = AdaendraImmutableDict({"hello": "world"})

# Get a value
immutable_dict["hello"]
#> world

# Copy dict
immutable_dict_copy = immutable_dict.copy()

# Create an immutable dict from "fromkeys" method
immutable_dict = AdaendraImmutableDict.fromkeys(["a", "b"], "1")
```

---

## Documentation
- [PyPi](./documentation/pypi.md)

---

## Credits 
This project is based on Marco Sulla's project: [frozen-dict](https://github.com/Marco-Sulla/python-frozendict).
