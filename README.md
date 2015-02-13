
# Generating symbol-mapping-file

awk -F '\t' '{printf "0x%s, r\"%s\",\n", $3, $1}' latex_symbols.txt > latex_symbol_map.txt