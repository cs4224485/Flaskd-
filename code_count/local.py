# Author: harry.cai
# DATE: 2018/9/2
'''
try:
    from greenlet import getcurrent as get_ident
except:
    from threading import get_ident


class Local(object):
    def __init__(self):
        object.__setattr__(self, 'storage', {})

    def __getattr__(self, item):
        ident = get_ident()
        if ident in self.storage:
            return self.storage[ident][item]
        return None

    def __setattr__(self, key, value):
        ident = get_ident()
        if ident not in self.storage:
            self.storage[ident] = {key:value}
        else:
            self.storage[ident][key] = value


obj = Local()

obj.session = 123
print(obj.sdfs)
print(obj.session)
'''