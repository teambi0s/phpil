
class Types:

    Null = 0
    Integer = 1 << 0
    Float = 1 << 1
    String = 1 << 2
    Boolean = 1 << 3
    Object = 1 << 4
    Function = 1 << 5 | String
    Class = 1 << 6
    Array = 1 << 7
    Unknown  = 1 << 8


class FunctionSignature:

    def __init__(self, numArgs, outerVars):
        self.numArgs = numArgs
        self.inputTypes = [Types.Unknown for i in range(numArgs)]
        self.returnType = Types.Unknown
        self.outerVars = outerVars
        self.isCons = True

    def setReturnType(self, type):
        self.returnType = type

    def getReturnType(self):
        return self.returnType

    def getOuterVars(self):
        return self.outerVars

    def setInputTypes(self, types):
        for i, type in enumerate(types):
            self.inputTypes[i] = type

    def getInputTypes(self):
        return self.inputTypes

    def getNumArgs(self):
        return self.numArgs

    def isConstructing(self):
        return self.isCons
