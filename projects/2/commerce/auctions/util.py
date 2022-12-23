def description_preview(description):
    if len(description) < 100: 
        return description 
    else:
        return description[0:100] + '...'