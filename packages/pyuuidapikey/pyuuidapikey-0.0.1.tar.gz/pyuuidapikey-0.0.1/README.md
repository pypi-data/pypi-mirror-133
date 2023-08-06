# pyuuidapikey


## Install
```
pip install pyuuidapikey
```

## Example

### **Generate Keys**

```
from pprint import pprint
from pyuuidapikey import UUIDAPIKey

uuidapikey = UUIDAPIKey()

keys: dict = uuidapikey.generate()
pprint(keys)
```

**Output**

```
{
	'apikey': 'TPICACD6-W97D3LB1-473P6SN5-1VNG9X4J',
	'uuid': '95f0aac2-3681-4ab1-89a2-6ea5614a191f'
}
```

### **Validate Keys**

```
from pyuuidapikey import UUIDAPIKey

apikey: str = 'TPICACD6-W97D3LB1-473P6SN5-1VNG9X4J'
uuid: str = '95f0aac2-3681-4ab1-89a2-6ea5614a191f'

uuidapikey = UUIDAPIKey()

is_valid: bool = uuidapikey.validate(apikey, uuid)
print(is_valid)
```

**Output**

```
True
```
Inspired the works from the JS library,

 - https://www.npmjs.com/package/uuid-apikey
 -  https://github.com/chronosis/uuid-apikey