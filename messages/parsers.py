import re

def match(regex, string):
    # simple case insensitive regex match
    # ignores groups
    if re.match(regex, string, re.IGNORECASE):
        return True
    else:
        return False

def is_yes(message):
    message = message.strip()
    return (False or 
        match('yes', message) or
        match('^yes', message) or
        match('^y$', message) or
        match('^y(e)?a(h)?', message) or
        match('^o?k(ay)?$', message) or
        match('^sure', message))

def is_no(message):
    message = message.strip()
    return (False or 
        match('^no(pe)?', message) or
        match('^n$', message) or
        match('^nah', message))

def is_number(message):
    message = message.strip()
    if message.isdigit():
        return int(message)
    else:
        return False

def is_reset(message):
    message = message.strip()
    return (False or 
        match('^reset$', message) or
        match('^restart$', message) or
        match('^again$', message))