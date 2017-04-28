import re

def match(regex, string):
    # simple case insensitive regex match
    # ignores groups
    if re.match(regex, string, re.IGNORECASE):
        return True
    else:
        return False

class ParseMessage(object):
    def __init__(self, body):
        self.body = body.strip()

    def is_yes(self):
        return (False or 
            match('yes', self.body) or
            match('^yes', self.body) or
            match('^y$', self.body) or
            match('^y(e)?a(h)?', self.body) or
            match('^o?k(ay)?$', self.body) or
            match('^sure', self.body))

    def is_no(self):
        return (False or 
            match('^no(pe)?', self.body) or
            match('^n$', self.body) or
            match('^nah', self.body))

    def is_number(self):
        if self.body.isdigit():
            return int(self.body)
        else:
            return False

    def is_reset(self):
        return (False or 
            match('^reset$', self.body) or
            match('^restart$', self.body) or
            match('^again$', self.body))
