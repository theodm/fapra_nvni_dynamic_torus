import re
import numpy as np

with open('parameter_results.txt', 'r') as f:
    data = f.read()
    pattern = r'[-=|]'
    # Ersetze alle Vorkommen von - mit einem leeren String
    mod_string = re.sub(pattern, '', data)
    mod_string = re.sub('\ \ +',',', mod_string)
    mod_string = re.sub(' ','',mod_string)
    f.close()

print(mod_string)

with open('parameter_results.csv', 'w') as f:
    for dataline in mod_string:
        f.write(dataline)

#pattern = r'-'
# Ersetze alle Vorkommen von - mit einem leeren String
#mod_string = re.sub(pattern, '', data)

#print(data)