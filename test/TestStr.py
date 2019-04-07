import time
from datetime import datetime

name = "tom"
val = 123
name1 = "kke"
val1 = 34

lists = []
tuple = (name, str(val), datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
tuple1 = (name1, str(val1))
lists.append(tuple)
lists.append(tuple1)
print(tuple)
print(lists)
