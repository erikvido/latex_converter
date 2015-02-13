Windows UTF-8 Signature BOM
0xef, 0xbb, 0xbf


# Generating symbol-mapping-file

awk -F '\t' '{printf "0x%s, r\"%s\",\n", $3, $1}' latex_symbols.txt > latex_symbol_map.txt

awk -F '\t' '{printf "unichr(%s): r, # %s\n", $5, $1}' Unicode_lookup.txt > unicode_mapping.py