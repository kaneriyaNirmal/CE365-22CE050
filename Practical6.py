class RecursiveDescentParser:
    def __init__(self, input_string):
        self.input = input_string.replace(" ", "") 
        self.index = 0
    
    def parse(self):
        if self.S() and self.index == len(self.input):
            print("Valid string")
        else:
            print("Invalid string")
    
    def S(self):
        if self.match('a'):
            return True
        elif self.match('('):
            if self.L() and self.match(')'):
                return True
        return False
    
    def L(self):
        if self.S():
            return self.L_prime()
        return False
    
    def L_prime(self):
        if self.match(','):
            if self.S():
                return self.L_prime()
            return False
        return True  
    
    def match(self, char):
        if self.index < len(self.input) and self.input[self.index] == char:
            self.index += 1
            return True
        return False


if __name__ == "__main__":
    user_input = input("Enter a string to validate: ")
    parser = RecursiveDescentParser(user_input)
    parser.parse()
