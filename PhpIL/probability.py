import random
import string

class Random:

    '''Returns True if the probability is achieved and False otherwise'''
    @staticmethod
    def probability(prob):
        if prob == 1:
            return True
        if random.uniform(0,1) < prob:
            return True
        return False

    '''if probability is true then call funcs[0] else call funcs[1]'''
    @staticmethod
    def withprobability(prob, *funcs):
        onTrue = funcs[0]
        onFalse = None
        if len(funcs) == 2:
            onFalse = funcs[1]

        if Random.probability(prob):
            return onTrue()
        elif onFalse is not None:
            return onFalse()

    '''select and execute a function from list of functions, with equal probability'''
    @staticmethod
    def withEqualProbability(*funcs):
        selected = Random.chooseUniform(funcs)
        return selected()

    '''select a list element with equal probability'''
    @staticmethod
    def chooseUniform(lst):
        if len(lst) == 0:
            return None
        return random.choice(list(lst))

    '''get a random integer between a and b'''
    @staticmethod
    def randomInt(a,b):
        return random.randint(a,b)

    '''
    select an element from a list with the later ones getting more priority by a factor of "factor" times

    if  0 < factor < 1, then priority is given to the starting elements

    if factor > 1 priority given to elements in towards the end
    '''
    @staticmethod
    def chooseBiased(lst, factor):
        size = len(lst)

        if size == 1:
            return lst[0]

        x = 0
        for i in range(size):
            x += factor**i

        prob = (factor**(size-1))*(1.0/(x))

        return Random.withprobability(prob, lambda: lst[size-1],
                                    lambda: Random.chooseBiased(lst[:-1], factor))

    @staticmethod
    def chooseWeightedBiased(d):

        weights = d.values()
        items = d.keys()
        prob = weights[0]*(1.0/sum(weights))

        return Random.withprobability(prob, lambda: items[0],
                                    lambda: Random.chooseWeightedBiased(dict(zip(items[1:],weights[1:]))))


    @staticmethod
    def randomFloat(a,b):
        return random.uniform(a, b)

    @staticmethod
    def randomBool():
        choice = random.randint(0, 1)
        if choice == 0:
            return True
        else:
            return False

    @staticmethod
    def randomString(length):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


if __name__ == '__main__':
    import sys
    def main():

        print Random.randomString(10)
        return
        print Random.chooseWeightedBiased({'a':1,
                                           'b':5,
                                           'c':2,
                                           'd':3})

        print Random.chooseBiased([111,222,333,444,555,666],1.5)
        print Random.probability(0.5)
        Random.withprobability(0.9, lambda: sys.stdout.write("YES\n"))
        Random.withprobability(0.1, lambda: sys.stdout.write("YES\n"), lambda: sys.stdout.write("NO\n"))
        print Random.chooseUniform(range(100,200))
        print Random.randomInt(100,200)

    main()
