
# passthon 0.0.1
# By Adrián Fernández

# This library is still under development, excuse the mistakes!

class password():
    
    password = ''       # for a single password. Empty by default.
    passwords = []      # for multiple passwords. Empty by default.
    
    def __init__(self, length, lc=True, uc=False, num=True, sym=False): 
        import string
        self.length = int(length)
        self.lowercase = bool(lc)
        self.uppercase = bool(uc)
        self.num = bool(num)
        self.sym = bool(sym)
        
        chars = []
        
        if self.lowercase:
            chars.append(string.ascii_lowercase)  # abcdefghijklmnopqrstuvwxyz
        if self.uppercase:
            chars.append(string.ascii_uppercase)  # ABCDEFGHIJKLMNOPQRSTUVWXYZ
        if self.num:
            chars.append(string.digits)           # 0123456789
        if self.sym:
            chars.append('#$%&@!?*._-')
        self.chars = chars = ''.join(chars)
            
    def gen(self):
        from random import choice
        self.password = ''
        self.password = ''.join(choice(self.chars) for i in range(self.length))
        return self.password

    def gen_multi(self, amount):
        from random import choice
        self.passwords = []
        for i in range(amount):
            self.passwords.append(''.join(choice(self.chars) for i in range(self.length)))
        return self.passwords
            
    def print(self):
        if self.passwords != []:
            for i in self.passwords:
                print(i)
        elif self.password == '':
            self.gen()
        print(self.password)