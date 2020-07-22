class Variable:

    def __init__(self,id):
        self.id = id

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        if self.id == other.id:
            return True
        return False

    def __str__(self):
        return "$v"+str(self.id)

    def __hash__(self):
        # print "AA"
        return hash(self.id)

    def __repr__(self):
        return "v"+str(self.id)

if __name__ == '__main__':
    print Variable(1)
