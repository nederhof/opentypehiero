from uni_extract import extract_groups, extract_unique_group_strings

groups = extract_unique_group_strings(['tests/hieropage.html'])
print(groups)

groups = extract_groups(['tests/hieropage.html'])
print(groups)
