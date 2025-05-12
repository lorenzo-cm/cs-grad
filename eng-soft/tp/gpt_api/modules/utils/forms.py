from __future__ import annotations

class LastMessage:
    def __init__(self, id, **kwargs):
        self.user_id = id
        self.lm = kwargs.get('message')
        self.ailm = kwargs.get('ailm')
        self.lmdt = kwargs.get('timestamp')
        
    def printAll(self):
        print(self.lm)
        print(self.ailm)
        print(self.lmdt)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'lm': self.lm,
            'ailm': self.ailm,
            'lmdt': self.lmdt,
        }
    
    def __str__(self):
        return f'Last_messages(user_id={self.user_id}, lm={self.lm}, ailm={self.ailm}, lmdt={self.lmdt})'
    
    def __repr__(self):
        return self.__str__()
    

class User:
    def __init__(self, id, name=None, confirmation_flag=None, ctt_time=None):
        self.id = str(id)
        self.name = name
        self.confirmation_flag = confirmation_flag
        self.ctt_time = ctt_time

    def __str__(self) -> str:
        return f'User: id: {self.id}, name: {self.name}, confirmation_flag: {self.confirmation_flag}, ctt_time: {self.ctt_time}'
    
    def __repr__(self) -> str:
        return f'User: id: {self.id}, name: {self.name}, confirmation_flag: {self.confirmation_flag}, ctt_time: {self.ctt_time}'
    
    def to_dict(self, **kwargs):
        attributes = ['name', 'id', 'confirmation_flag', 'ctt_time']
        return {attr: getattr(self, attr) for attr in attributes if kwargs.get(attr, True)}

