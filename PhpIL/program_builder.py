import program
import instructions
import typesData
import analyzer
import variable
import operation
import probability
import settings
from code_generators import CodeGenerator

class ProgramBuilder:

    def __init__(self, prog=False):
        if prog == False:
            self.program = program.Program()
        else:
            self.program = prog

        self.nextFreeVariable = self.program.nextVariable
        self.instructionList = []
        for i in self.program.instructionList:
            self.instructionList.append(i)

        self.seenIntegers = set([])
        self.seenFloats = set([])
        self.seenStrings = set([])

        self.scopeAnalyzer = analyzer.ScopeAnalyzer(self.program)
        self.scopeAnalyzer.doAnalyze()

        self.contextAnalyzer = analyzer.ContextAnalyzer(self.program)
        self.contextAnalyzer.doAnalyze()

        self.typeAnalyzer = analyzer.TypeAnalyzer(self.program)
        self.typeAnalyzer.doAnalyze()


    '''Append a given instruction to the current program after performing analysis'''
    def instructionAppend(self, inst):
        # print inst
        self.scopeAnalyzer.analyze(inst)
        self.contextAnalyzer.analyze(inst)
        self.typeAnalyzer.analyze(inst)
        self.instructionList.append(inst)

    ''''Utility functions start'''

    '''finish this program builder and save the instructions to the program'''
    def finish(self):
        for i in self.instructionList:
            self.program.append(i)

        return self.program

    '''get variables of type "type" '''
    def randVar(self, type=typesData.Types.Unknown, strict=0):

        candidates = []
        iter = 2*len(self.scopeAnalyzer.scopes)
        while len(candidates) == 0 and iter > 0:
            candidates = probability.Random.chooseBiased(self.scopeAnalyzer.scopes, 6)
            candidates = filter(lambda x: self.typeAnalyzer.getType(x) == type or self.typeAnalyzer.getType(x) == typesData.Types.Unknown, candidates)
            iter -= 1

        if len(candidates) == 0:
            if type == typesData.Types.Boolean:
                candidates = [self.loadBoolean(probability.Random.randomBool())]
            if type == typesData.Types.String:
                candidates = [self.loadString(self.getString())]
            if type == typesData.Types.Float:
                candidates = [self.loadFloat(self.getFloat())]
            if type == typesData.Types.Integer:
                candidates = [self.loadInteger(self.getInt())]

            if type == typesData.Types.Unknown:
                while len(candidates) == 0:
                    candidates = probability.Random.chooseBiased(self.scopeAnalyzer.scopes, 5)



        if len(candidates) == 0:
            return False
        # print candidates
        ret = probability.Random.chooseUniform(candidates)
        # print ret, self.typeAnalyzer.getType(ret)
        return ret

    def generateRandomInst(self):
        ret = False
        if len(self.scopeAnalyzer.getVisibleVars()) == 0:
            codegens = [
                CodeGenerator.nullValueGenerator,
                CodeGenerator.booleanLiteralGenerator,
                CodeGenerator.floatLiteralGenerator,
                CodeGenerator.stringLiteralGenerator,
                CodeGenerator.integerLiteralGenerator
            ]

            return probability.Random.chooseBiased(codegens,1.5)(self)

        while not ret:
            choice = probability.Random.chooseWeightedBiased(settings.Settings.allCodeGenerators)
            ret = choice(self)

    def getInt(self):
        def selectFromSeen():
            return probability.Random.chooseUniform(list(self.seenIntegers))
        def createNew():
            return probability.Random.randomInt(-0x1000, 0x1000)

        ret = None
        while ret == None:
            ret = probability.Random.withprobability(0.50, selectFromSeen, createNew)

        self.seenIntegers.add(ret)

        return ret


    def getFloat(self):
        def selectFromSeen():
            return probability.Random.chooseUniform(list(self.seenFloats))
        def createNew():
            return probability.Random.randomFloat(-0x1000, 0x1000)

        ret = None
        while ret == None:
            ret = probability.Random.withprobability(0.50, selectFromSeen, createNew)

        self.seenFloats.add(ret)

        return ret

    def getString(self):
        def selectFromSeen():
            return probability.Random.chooseUniform(list(self.seenStrings))
        def createNew():
            return probability.Random.randomString(probability.Random.randomInt(0,10))

        ret = None
        while ret == None:
            ret = probability.Random.withprobability(0.50, selectFromSeen, createNew)

        self.seenStrings.add(ret)

        return ret

    def isInLoop(self):
        return self.contextAnalyzer.isInLoopContext()

    def isInFunction(self):
        return self.contextAnalyzer.isInFunctionContext()

    def lastContextisLoop(self):
        return self.contextAnalyzer.lastContextisLoop()

    def getOuterVars(self):
        return self.scopeAnalyzer.getOuterVisibleVars()

    def getVisibleVars(self):
        return self.scopeAnalyzer.getVisibleVars()

    def generateCallArguments(self, function):
        signature = self.typeAnalyzer.getSignature(function)
        if not isinstance(signature, typesData.FunctionSignature):
            return False
        argsTypes = signature.getInputTypes()
        arguments = []
        for type in argsTypes:
            arguments.append(self.randVar(type))

        return arguments


    ''''Utility functions end'''


    '''Returns the next free variable for this program'''
    def nextVariable(self):
        self.nextFreeVariable += 1
        return variable.Variable(self.nextFreeVariable-1)

    '''Assign variables and convert the given operation into an instruction'''
    def perform(self, ops, inputs=False):
        outputs = []
        tempVars = []
        for i in range(ops.numOutputs):
            outputs.append(self.nextVariable())
        for i in range(ops.numTempvars):
            tempVars.append(self.nextVariable())

        if outputs == []:
            outputs = False
        if tempVars == []:
            tempVars = False

        inst = instructions.Instruction(ops, inputs, outputs, tempVars)
        self.instructionAppend(inst)

        return inst

    '''Instructions in PHPIL added to this program'''

    def nop(self):
        return self.perform(operation.Nop()).getOutput()

    def loadInteger(self, value):
        return self.perform(operation.LoadInteger(value)).getOutput()

    def loadFloat(self, value):
        return self.perform(operation.LoadFloat(value)).getOutput()

    def loadString(self, value):
        return self.perform(operation.LoadString(value)).getOutput()

    def loadBoolean(self, value):
        return self.perform(operation.LoadBoolean(value)).getOutput()

    def loadNull(self):
        return self.perform(operation.LoadNull()).getOutput()

    def createObject(self, object, args, fieldValues):
        return self.perform(operation.CreateObject(object, args, fieldValues)).getOutput()

    def createArray(self, initialValues):
        return self.perform(operation.CreateArray(len(initialValues)), initialValues).getOutput()

    def callFunction(self, funcName, args):
        return self.perform(operation.CallFunction(len(args) + 1), [funcName] + args).getOutput()

    def doPrint(self, value):
        return self.perform(operation.Print(), [value]).getOutput()

    #beginFunction is not finished in operation.py
    def beginFunction(self):
        return self.perform(operation.BeginFunction()).getOutput()

    #endFunction is not finished in operation.py
    def endFunction(self):
        return self.perform(operation.EndFunction())


    def beginIf(self, conditional):
        return self.perform(operation.BeginIf(), [conditional])

    def beginElse(self):
        return self.perform(operation.BeginElse())

    def endIf(self):
        return self.perform(operation.EndIf())

    def beginWhile(self, lhs, comparater, rhs):
        return self.perform(operation.BeginWhile(comparater), [lhs, rhs])

    def endWhile(self):
        return self.perform(operation.EndWhile())

    def beginFor(self, start, comparater, end, op, rhs):
        return self.perform(operation.BeginFor(op, comparater), [start, end, rhs])

    def copy(self, inp, out):
        return self.perform(operation.Copy(), [inp, out])

    def endFor(self):
        self.perform(operation.EndFor())

    def beginDoWhile(self):
        return self.perform(operation.BeginDoWhile())

    def endDoWhile(self, lhs, comparater, rhs):
        return self.perform(operation.EndDoWhile(comparater), [lhs, rhs])

    #beginForEach notDefined in operation.py
    def beginForEach(self):
        return self.perform(operation.BeginForEach())

    def endForEach(self):
        return self.perform(operation.EndForEach())

    def doReturn(self, value):
        return self.perform(operation.Return(), [value])

    def doBreak(self):
        return self.perform(operation.Break(), [])

    def doContinue(self):
        return self.perform(operation.Continue(), [])

    def beginTry(self):
        return self.perform(operation.BeginTry())

    def beginCatch(self):
        return self.perform(operation.BeginCatch())

    def endTryCatch(self):
        return self.perform(operation.EndTryCatch())

    #BeginClass not completed in operation.py
    def beginClass(self):
        return self.perform(operation.BeginClass()).getOutput()

    #EndClass not completed in operation.py
    def endClass(self):
        return self.perform(operation.EndClass()).getOutput()

    def unaryOperation(self, op, input):
        return self.perform(operation.UnaryOperation(op), [input]).getOutput()

    #check binaryOperation function once again
    def binaryOperation(self, lhs, rhs, op):
        return self.perform(operation.BinaryOperation(op), [lhs, rhs]).getOutput()

    def functionDefination(self, signature):
        return self.perform(operation.BeginFunction(signature)).getOutput()

    def doInclude(self, value):
        return self.perform(operation.Include(), [value])

    #check doEval
    def doEval(self, string, arguments):
        return self.perform(operation.Eval(string, len(argummets)), arguments).getOutput()

    def phi(self, var):
        return self.perform(operation.Phi(), [var]).getOutput()

    def createDict(self, dictElements):
        return self.perform(operation.CreateDict(len(dictElements)), dictElements).getOutput()

    def getArrayElem(self, arr, elem):
        return self.perform(operation.GetArrayElem(), [arr,elem]).getOutput()

    def setArrayElem(self, arr, elem, value):
        return self.perform(operation.SetArrayElem(), [arr,elem,value])


    #ThrowException not completed in operation.py
    def throwException(self, value):
        return self.perform(operation.ThrowException(), [value])

if __name__ == '__main__':
    def main():
        a = ProgramBuilder()
        out1 = []
        out2 = []
        out3 = []
        for i in range(10):
            out1.append(a.getInt())
            out2.append(a.getFloat())
            out3.append(a.getString())
        print out1
        print out2
        print out3

    main()
