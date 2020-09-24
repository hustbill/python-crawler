# string natural sort

import re

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

elements = ['Elm11', 'Elm12', 'Elm2', 'elm0', 'elm1', 'elm10', 'elm13', 'elm9']

print ("original elements: ")
print (elements)

natural_sorted_elements = natural_sort(elements)

print ("natural sorted elements: ")

print (natural_sorted_elements)