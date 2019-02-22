## Usage

```python
import json
from dynamic import *

inv = Inventory("myinventory")


my_host = Host("my-srv-test", { "ansible_host" : "192.168.1.1" })
my_group = Group("my_group")
my_group.add_host(my_host)

inv.add_group(my_group)

print json.dumps(inv.toJSON())

```
