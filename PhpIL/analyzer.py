import program
import opcodes
import variable
import operation
import instructions
from typesData import Types

class Analyzer(object):

    def __init__(self, programToAnalyse):
        self.program = programToAnalyse

    ''' Perform analysis on the entire program'''
    def doAnalyze(self):
        for inst in self.program.instructionList:
            self.analyze(inst)

    ''' Virtual function that analyzes a given instruction '''
    def analyze(self,inst):
        pass

class ScopeAnalyzer(Analyzer):

    def __init__(self, programToAnalyse):
        super(ScopeAnalyzer, self).__init__(programToAnalyse)
        self.scopes = [set([])]
        self.numScopes = 1
        self.stack = []

    def getVisibleVars(self):
        # print [j for i in self.scopes for j in i]
        return [j for i in self.scopes for j in i]

    def getOuterVisibleVars(self):
        outerScopes = self.scopes[:-1]
        # print self.scopes
        return [j for i in outerScopes for j in i]

    def analyze(self, inst):
        # print self.scopes

        if inst.isBlockEnd():
            self.scopes.pop()
            if inst.getOpcode() == operation.EndFunction:
                out = self.stack.pop()
                self.scopes[-1].update([out])

        if inst.getOpcode() == opcodes.opcodes.BeginFunction:
            self.stack.append(inst.getOutput())
        else:
            self.scopes[-1].update(inst.getAllOutputs())

        if inst.isBlockBegin():
            self.scopes.append(set([]))

        self.scopes[-1].update(inst.getAllTemps())

        # print self.scopes

class ContextAnalyzer(Analyzer):

    isGlobal = 0
    isInLoop = 1 << 0
    isInFunction = 1 << 1

    def __init__(self,programToAnalyse):
        super(ContextAnalyzer, self).__init__(programToAnalyse)
        self.context = [[0]]
        self.lastContext = [[0]]

    def analyze(self, inst):

        def debug():
            a=[self.context]
            if self.context[-1][0] == 0:
                a.append("Global")

            if self.context[-1][0] & ContextAnalyzer.isInLoop:
                a.append("InLoop")

            if self.context[-1][0] & ContextAnalyzer.isInFunction:
                a.append("InFunction")
            print a

        if inst.isLoopBegin() or inst.isBeginFunction():
            self.context.append([self.context[-1][0]])
            self.lastContext.append([])

        if inst.isBeginFunction():
            self.context[-1][0] |= ContextAnalyzer.isInFunction
            self.lastContext[-1].append(ContextAnalyzer.isInFunction)

        if inst.isEndFunction():
            self.context[-1][0] &= ~ContextAnalyzer.isInFunction

        if inst.isLoopBegin():
            self.context[-1][0] |= ContextAnalyzer.isInLoop
            self.lastContext[-1].append(ContextAnalyzer.isInLoop)

        if inst.isLoopEnd():
            self.context[-1][0] &= ~ContextAnalyzer.isInLoop

        if inst.isEndFunction() or inst.isLoopEnd():
            self.context.pop()
            self.lastContext.pop()

        # debug()

    def isGlobalContext(self):
        return self.context[-1][0] == 0

    def isInLoopContext(self):
        return self.context[-1][0] & ContextAnalyzer.isInLoop

    def isInFunctionContext(self):
        return self.context[-1][0] & ContextAnalyzer.isInFunction

    def lastContextisLoop(self):
        return self.lastContext[-1][0] == ContextAnalyzer.isInLoop


class TypeAnalyzer(Analyzer):

    def __init__(self, programToAnalyze):
        super(TypeAnalyzer, self).__init__(programToAnalyze)
        self.variableTypes = [{}]
        self.stack = []
        self.returnStack = []
        self.signatureTracker = {}

    def setType(self, vars, type):
        for i in vars:
            self.variableTypes[-1][i] = type

    def getType(self, var):
        for i in self.variableTypes:
            if var in i:
                return i[var]

    def getSignature(self, var):
        if self.getType(var) == Types.Function:
            return self.signatureTracker[var]
        return False

    def analyze(self, inst):

        if inst.getOpcode() == opcodes.opcodes.LoadInteger:
            self.setType(inst.getAllOutputs(), Types.Integer)
        if inst.getOpcode() == opcodes.opcodes.LoadFloat:
            self.setType(inst.getAllOutputs(), Types.Float)
        if inst.getOpcode() == opcodes.opcodes.LoadString:
            self.setType(inst.getAllOutputs(), Types.String)
        if inst.getOpcode() == opcodes.opcodes.LoadBoolean:
            self.setType(inst.getAllOutputs(), Types.Boolean)
        if inst.getOpcode() == opcodes.opcodes.LoadNull:
            self.setType(inst.getAllOutputs(), Types.Null)
        # if inst.getOpcode() == opcodes.opcodes.LoadObject:
        #     self.setType(inst.getAllOutputs(), Types.Object)
        if inst.getOpcode() == opcodes.opcodes.BeginClass:
            self.setType(inst.getAllOutputs(), Types.Class)

        if inst.getOpcode() == opcodes.opcodes.UnaryOperation:
            if self.getType(inst.getInput()) == Types.Unknown:
                self.setType(inst.getAllInputs(), Types.Integer)
            self.setType(inst.getAllOutputs(), self.getType(inst.getInput(0)))

        if inst.getOpcode() == opcodes.opcodes.BeginFor:
            self.setType(inst.getAllTemps(), self.getType(Types.Unknown))

        if inst.getOpcode() == opcodes.opcodes.BinaryOperation:

            op = inst.operation.op

            if op == operation.Comparater.equal or \
               op == operation.Comparater.notEqual or \
               op == operation.Comparater.greaterThan or \
               op == operation.Comparater.greaterThanOrEqual or \
               op == operation.Comparater.lessThan or \
               op == operation.Comparater.lessThanOrEqual or \
               op == operation.Comparater.strictEqual or \
               op == operation.BinaryOperator.LogicOr or \
               op == operation.BinaryOperator.LogicAnd:

              self.setType(inst.getAllOutputs(),Types.Boolean)

            if op == operation.BinaryOperator.Add or \
               op == operation.BinaryOperator.Sub or \
               op == operation.BinaryOperator.Mul or \
               op == operation.BinaryOperator.Div or \
               op == operation.BinaryOperator.LShift or \
               op == operation.BinaryOperator.RShift:

              outType = Types.Integer
              inps = inst.getAllInputs()
              if self.getType(inps[0]) == Types.Float or self.getType(inps[1]) == Types.Float:
                  outType = Types.Float
              self.setType(inst.getAllOutputs(),outType)

            if op == operation.BinaryOperator.BitOr or \
               op == operation.BinaryOperator.BitAnd or \
               op == operation.BinaryOperator.Xor:

              outType = Types.Integer
              inps = inst.getAllInputs()
              if self.getType(inps[0]) == Types.String or self.getType(inps[1]) == Types.String:
                   outType = Types.String
              self.setType(inst.getAllOutputs(),outType)

            if op == operation.BinaryOperator.Mod:

              self.setType(inst.getAllOutputs(),Types.Integer)

        if inst.getOpcode() == opcodes.opcodes.Phi:
            inp = inst.getInput()
            self.setType(inst.getAllOutputs(), self.getType(inp))
            if self.getType(inp) == Types.Function:
                self.signatureTracker[inst.getOutput()] = self.getSignature(inp)

        if inst.getOpcode() == opcodes.opcodes.Copy:
            inp = inst.getInput(1)
            self.setType([inst.getInput(0)], self.getType(inp))
            if self.getType(inp) == Types.Function:
                self.signatureTracker[inst.getInput(0)] = self.getSignature(inp)

        if inst.isBeginFunction():
            self.setType(inst.getAllOutputs(), Types.Function)
            self.setType(inst.getAllTemps(), Types.Unknown)
            self.stack.append(inst)
            self.variableTypes.append({})
            self.returnStack.append([])
            self.signatureTracker[inst.getOutput()] = inst.operation.signature

        if inst.isEndFunction():
            stackFrame = self.variableTypes.pop()
            returnType = self.returnStack.pop()[0]
            func = self.stack.pop()
            signature = func.operation.signature
            outputVar = func.getOutput()
            inputTypes = [self.getType(var) for var in func.getAllTemps()]

            signature.isCons = False
            signature.setReturnType(returnType)
            signature.setInputTypes(inputTypes)

        if inst.getOpcode() == opcodes.opcodes.Return:
            self.returnStack[-1].append(self.getType(inst.getInput(0)))

        if inst.getOpcode() == opcodes.opcodes.CallFunction:
            func = self.signatureTracker[inst.getInput()]
            returnType = func.getReturnType()
            self.setType(inst.getAllOutputs(), returnType)

        if inst.getOpcode() == opcodes.opcodes.BeginIf:
            if self.getType(inst.getInput()) == Types.Unknown:
                self.setType(inst.getAllInputs(), Types.Boolean)

        if inst.getOpcode() == opcodes.opcodes.CreateArray:
            self.setType(inst.getAllOutputs(), Types.Array)
        

        # print self.variableTypes



# Tests ->

if __name__ == '__main__':
    import typesData
    def main():
        prog = program.Program([
            instructions.Instruction(operation.LoadInteger(1),False,[variable.Variable(0)]),
            instructions.Instruction(operation.LoadInteger(9),False,[variable.Variable(3)]),
            instructions.Instruction(operation.LoadString("thisisastring"),False,[variable.Variable(1)]),
            instructions.Instruction(operation.LoadInteger(True),False,[variable.Variable(4)]),
            instructions.Instruction(operation.BeginWhile(">"),[variable.Variable(0), variable.Variable(3)]),
            instructions.Instruction(operation.LoadInteger(1337),False,[variable.Variable(6)]),
            instructions.Instruction(operation.BeginIf(),[variable.Variable(2)]),
            instructions.Instruction(operation.LoadString("thisisastring"),False,[variable.Variable(9)]),
            instructions.Instruction(operation.EndIf()),
            instructions.Instruction(operation.BinaryOperation(">"),[variable.Variable(0),variable.Variable(3)],[variable.Variable(5)]),
            instructions.Instruction(operation.EndWhile()),
            instructions.Instruction(operation.LoadInteger(10),False,[variable.Variable(31337)]),
        ])
        prog = program.Program([
            instructions.Instruction(operation.LoadInteger(0), False, [variable.Variable(0)]),
            instructions.Instruction(operation.LoadInteger(1), False, [variable.Variable(1)]),
            instructions.Instruction(operation.LoadInteger(10), False, [variable.Variable(2)]),
            instructions.Instruction(operation.LoadInteger(10), False, [variable.Variable(3)]),
            instructions.Instruction(operation.LoadInteger(20), False, [variable.Variable(4)]),
            instructions.Instruction(operation.LoadInteger(5), False, [variable.Variable(5)]),
            instructions.Instruction(operation.Phi(), [variable.Variable(3)], [variable.Variable(6)]),
            instructions.Instruction(operation.Phi(), [variable.Variable(4)], [variable.Variable(7)]),
            instructions.Instruction(operation.BeginFor("++", "<"), [variable.Variable(0),variable.Variable(2),variable.Variable(8)]),
            instructions.Instruction(operation.BinaryOperation("<"), [variable.Variable(8), variable.Variable(5)], [variable.Variable(6)]),
            instructions.Instruction(operation.BeginIf(), [variable.Variable(6)], False),
            instructions.Instruction(operation.LoadInteger(0), False, [variable.Variable(9)]),
            instructions.Instruction(operation.BeginWhile("<"),[variable.Variable(9), variable.Variable(5)], False ),
            instructions.Instruction(operation.BinaryOperation("+"), [variable.Variable(6), variable.Variable(1)], [variable.Variable(10)]),
            instructions.Instruction(operation.Copy(), [variable.Variable(6), variable.Variable(10)]),
            instructions.Instruction(operation.BinaryOperation("+"), [variable.Variable(9), variable.Variable(1)], [variable.Variable(11)]),
            instructions.Instruction(operation.Copy(), [variable.Variable(6), variable.Variable(10)]),

            instructions.Instruction(operation.BeginFunction(typesData.FunctionSignature(2,[variable.Variable(11)])),False,[variable.Variable(1)],[variable.Variable(10),variable.Variable(11)]),
            instructions.Instruction(operation.BinaryOperation("+"),[variable.Variable(10),variable.Variable(11)],[variable.Variable(2)]),
            instructions.Instruction(operation.LoadString("somestring"),False,[variable.Variable(3)]),
            instructions.Instruction(operation.Return(),[variable.Variable(2)]),
            instructions.Instruction(operation.EndFunction()),
            instructions.Instruction(operation.LoadInteger(1337),False,[variable.Variable(4)]),
            instructions.Instruction(operation.CallFunction(2),[variable.Variable(1), variable.Variable(4), variable.Variable(0)],[variable.Variable(6)]),

            instructions.Instruction(operation.EndWhile(), False, False),

            instructions.Instruction(operation.BeginElse(), False, False),
            instructions.Instruction(operation.LoadInteger(0), False, [variable.Variable(9)]),
            instructions.Instruction(operation.BeginWhile("<"),[variable.Variable(9), variable.Variable(5)], False ),
            instructions.Instruction(operation.BinaryOperation("+"), [variable.Variable(7), variable.Variable(1)], [variable.Variable(10)]),
            instructions.Instruction(operation.Copy(), [variable.Variable(7), variable.Variable(10)]),
            instructions.Instruction(operation.BinaryOperation("+"), [variable.Variable(9), variable.Variable(1)], [variable.Variable(11)]),
            instructions.Instruction(operation.Copy(), [variable.Variable(6), variable.Variable(10)]),
            instructions.Instruction(operation.EndWhile(), False, False),

            instructions.Instruction(operation.EndIf(), False, False),
            instructions.Instruction(operation.EndFor(), False, False),
            instructions.Instruction(operation.LoadInteger(1),False,[variable.Variable(90)]),
        ])
        program.Program([
            instructions.Instruction(operation.LoadInteger(1),False,[variable.Variable(0)]),
            instructions.Instruction(operation.BeginFunction(typesData.FunctionSignature(2,[variable.Variable(11)])),False,[variable.Variable(1)],[variable.Variable(10),variable.Variable(11)]),
            instructions.Instruction(operation.BinaryOperation("+"),[variable.Variable(10),variable.Variable(11)],[variable.Variable(2)]),
            instructions.Instruction(operation.LoadString("somestring"),False,[variable.Variable(3)]),
            instructions.Instruction(operation.Return(),[variable.Variable(2)]),
            instructions.Instruction(operation.EndFunction()),
            instructions.Instruction(operation.LoadInteger(1337),False,[variable.Variable(4)]),
            instructions.Instruction(operation.CallFunction(2),[variable.Variable(1), variable.Variable(4), variable.Variable(0)],[variable.Variable(6)]),
            instructions.Instruction(operation.LoadInteger(1337),False,[variable.Variable(7)]),
        ])
        print prog
        ctx = ContextAnalyzer(prog)
        ctx.doAnalyze()
        #
        # sc = ScopeAnalyzer(prog)
        # sc.doAnalyze()


        # ti = TypeAnalyzer(prog)
        # ti.doAnalyze()


    main()
