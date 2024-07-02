
def name_validation(name):
    if name.isalpha() and len(name) > 1:
        return name
    return None
