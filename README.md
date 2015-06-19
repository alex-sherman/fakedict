#Fakedict


A Python module allowing the simple creation of dictionaries with getter/setter functions.

Install using pip:

```
pip install fakedict
```

# Usage

Abstracting certain kinds of interactions as dictionary operations can be a useful tool for some applications.
A simple example is handling a JSON file containing a dictionary. Rather calling json.dump and json.load, we'll instead
use a dictionary abstraction for interacting with the file. Many other use cases exist, in fact this module was developed
in order to be used with python-jrpc for the purpose of abstracting some RPC calls into dictionary operations.

## JSON File Example

### dict.json
```json
{
  "key": "value"
}
```

### reader.py
```python
import fakedict
jfile = fakedict.JSONFile("dict.json")
print jfile["key"]
jfile["something"] = "faff"
```

This will print "value" and modify the contents of dict.json to the following:
```json
{
  "key": "value",
  "something": "faff"
}
```
