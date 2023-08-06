
def yes_or_no(question:str, answer:bool):
    '''
    Should be used in debug string to see if certain
    conditions are met. Useful in f strings.
    '''
    return question + (' yes' if answer else ' no')
    