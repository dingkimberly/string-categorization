from Levenshtein import ratio

# Takes a bunch of strings and sorts them into groups of similar strings according to Levenshtein distance.
# Tolerance is a float from 0 to 1. 
def fuzzy_string_group(strings, tolerance):
    
    groups = {}
    
    for i in range(len(strings)):
        curr = strings[i]
        append_to = curr

        for key, key_group in groups.items():
            if ratio(curr, key) > tolerance:
                append_to = key
                break
                
        if groups.get(append_to) == None:
            groups[append_to] = [curr]
        else:
            groups[append_to].append(curr)
    
    return groups