import re

text = "876876 PUBLISHER   title $3.99 jklhljhljh"

pattern = re.compile(r"PUBLISHER\s*(.+?)\s*[$](\d+.\d+)")

searched = pattern.search(text)

name = searched.group(1)
num = searched.group(2)

print(name)
print(num)


