Latex_converter
===============

Is a very simple python-skript that replaces some reserved latex-symbols with their corresponding latex-command. 

### How to use it

To run the scipt type:
```
python convert.py source.txt
```
The file `source.txt` must be utf-8 encoded. Other encodings can be set with additional arguments, c.f. advanced options.

For explanation on advanced options type:
```
python convert.py help
```

### Contribue

The replacement is not complete, but can easly be adjusted by adding it to the mapping in [convert.py]. The file unicode_mapping.py contains a list of some utf-8 symbols and their unicode-hex-value, sometimes the corrsponding latex-command is given. The list is not complete but this might helps you to speed up the unicode lookup.

### Understanding Unicode

I found the article [Understanding Python and Unicode](http://www.carlosble.com/2010/12/understanding-python-and-unicode/) from Carlos Blé well written and easy to understand for non-programmers.

