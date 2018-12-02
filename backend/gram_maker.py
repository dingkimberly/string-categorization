def get_n_grams_count(n, df):
    
    count = 0
    
    for _, row in df.iterrows():
        
        numwords = len(row[0])

        if numwords < n:
            continue
        else:
            count += numwords - n + 1
    
    return count

def make_n_grams(n, df):
    
    new_grams = pd.DataFrame(columns=['item_title', 'category'])
    n_grams_count = get_n_grams_count(n, df)
    grams_col = [[] for _ in range(n_grams_count)]
    cat_col = [None for _ in range(n_grams_count)]
    
    index = 0
    
    for _, row in df.iterrows():

        words = row[0]
        category = row[1]
        numwords = len(words)

        if numwords < n:
            continue
        else:
            for j in range(numwords-n+1):
                grams_col[index] = words[j:j+n]
                cat_col[index] = category
                index += 1           
                
    grams_dict = {}
    grams_dict['item_title'] = grams_col
    grams_dict['category'] = cat_col
    
    new_grams = pd.DataFrame.from_dict(grams_dict)
        
    return new_grams