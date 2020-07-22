import opcodes

class Operation(object):

    class Attributes:
        isPrimitive        = 1 << 0
        isLiteral          = 1 << 1
        isParametric       = 1 << 2
        isCall             = 1 << 3
        isBlockBegin       = 1 << 4
        isBlockEnd         = 1 << 5
        isLoopBegin        = 1 << 6
        isLoopEnd          = 1 << 7
        isInternal         = 1 << 8
        isJump             = 1 << 9
        isImmutable        = 1 << 10
        isVarargs          = 1 << 11

    def __init__(self, numInputs, numOutputs, numTempvars, attributes=[]):
        self.opcode = 0
        self.numInputs = numInputs
        self.numOutputs = numOutputs
        self.numTempvars = numTempvars
        self.attributes = attributes
        self.flags = 0
        for i in attributes:
            self.flags |= i

    def getFlags(self):
        return self.flags

    def __str__(self):
        outstring = ""
        output = ""
        input = ""

        for i in range(self.numOutputs):
            output += "out" + str(i) + ", "

        if self.numOutputs > 0:
            output = ''.join(output.rsplit(',', 1)) + "= "

        for i in range(self.numInputs):
            input += "inp" + str(i) + ", "

        if self.numInputs > 0:
            input = ''.join(input.rsplit(',', 1)) + ""

        return output + opcodes.opcodes.opcodeList[self.opcode] + " " + input

class Nop(Operation):
    def __init__(self):
        super(Nop, self).__init__(numInputs=0, numOutputs=0, numTempvars=0, attributes=[Operation.Attributes.isPrimitive])
        self.opcode = opcodes.opcodes.Nop

class LoadInteger(Operation):
    def __init__(self, value):
        super(LoadInteger, self).__init__(numInputs=0, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.LoadInteger
        self.value = value

    def __str__(self):
        return "out0 = " + opcodes.opcodes.opcodeList[self.opcode] + " " + "'" + str(self.value) + "'"

class LoadFloat(Operation):
    def __init__(self, value):
        super(LoadFloat, self).__init__(numInputs=0, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.LoadFloat
        self.value = value

    def __str__(self):
        return "out0 = " + opcodes.opcodes.opcodeList[self.opcode] + " " + "'" + str(self.value) + "'"

class LoadString(Operation):
    def __init__(self, value):
        super(LoadString, self).__init__(numInputs=0, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.LoadString
        self.value = value

    def __str__(self):
        return "out0 = " + opcodes.opcodes.opcodeList[self.opcode] + " " + "'" + str(self.value) + "'"

class LoadBoolean(Operation):
    def __init__(self, value):
        super(LoadBoolean, self).__init__(numInputs=0, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.LoadBoolean
        self.value = value

    def __str__(self):
        return "out0 = " + opcodes.opcodes.opcodeList[self.opcode] + " " + "'" + str(self.value) + "'"

class LoadNull(Operation):
    def __init__(self):
        super(LoadNull, self).__init__(numInputs=0, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.LoadNull

# class LoadObject (Operation):
#     def __init__(self, value):
#(LoadObject , self)         super.__init__(numInputs=0, numOutputs=1, numTempvars=0)
#         self.opcode = opcodes.opcodes.LoadObject
#         self.value = value

class CreateObject(Operation):
    def __init__(self, object, args):
        super(CreateObject, self).__init__(numInputs=1, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.CreateObject
        self.object = object
        self.args = args

class CreateArray(Operation):
    def __init__(self, numInitialValues):
        super(CreateArray, self).__init__(numInputs=numInitialValues, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.CreateArray

class CallFunction(Operation):
    def __init__(self, numArgs):
        super(CallFunction, self).__init__(numInputs=numArgs+1, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.CallFunction

class BeginIf(Operation):
    def __init__(self):
        super(BeginIf, self).__init__(numInputs=1, numOutputs=0, numTempvars=0, attributes=[Operation.Attributes.isBlockBegin])
        self.opcode = opcodes.opcodes.BeginIf


class BeginElse(Operation):
    def __init__(self):
        super(BeginElse, self).__init__(numInputs=0, numOutputs=0, numTempvars=0, attributes=[Operation.Attributes.isBlockBegin, Operation.Attributes.isBlockEnd])
        self.opcode = opcodes.opcodes.BeginElse


class EndIf(Operation):
    def __init__(self):
        super(EndIf, self).__init__(numInputs=0, numOutputs=0, numTempvars=0, attributes=[Operation.Attributes.isBlockEnd])
        self.opcode = opcodes.opcodes.EndIf


class BeginWhile(Operation):
    def __init__(self, comparater):
        super(BeginWhile, self).__init__(numInputs=2, numOutputs=0, numTempvars=0, attributes=[Operation.Attributes.isBlockBegin, Operation.Attributes.isLoopBegin])
        self.opcode = opcodes.opcodes.BeginWhile
        self.comparater = comparater

    def __str__(self):
        input = " inp0, " + str(self.comparater) + ", inp1"
        return opcodes.opcodes.opcodeList[self.opcode] + input


class EndWhile(Operation):
    def __init__(self):
        super(EndWhile, self).__init__(numInputs=0, numOutputs=0, numTempvars=0, attributes=[Operation.Attributes.isBlockEnd, Operation.Attributes.isLoopEnd])
        self.opcode = opcodes.opcodes.EndWhile

class BeginFor(Operation):
    def __init__(self, comparater, op):
        super(BeginFor, self).__init__(numInputs=3, numOutputs=0, numTempvars=1, attributes=[Operation.Attributes.isBlockBegin, Operation.Attributes.isLoopBegin])
        self.opcode = opcodes.opcodes.BeginFor
        self.op = op
        self.comparater = comparater

    def __str__(self):
        input = " inp0, "+str(self.op)+" , inp1, "+str(self.comparater)+" ,inp2"
        return opcodes.opcodes.opcodeList[self.opcode] + input

class EndFor(Operation):
    def __init__(self):
        super(EndFor, self).__init__(numInputs=0, numOutputs=0, numTempvars=0, attributes=[Operation.Attributes.isBlockEnd, Operation.Attributes.isLoopEnd])
        self.opcode = opcodes.opcodes.EndFor

class BeginDoWhile(Operation):
    def __init__(self):
        super(BeginDoWhile, self).__init__(numInputs=0, numOutputs=0, numTempvars=0, attributes=[Operation.Attributes.isBlockBegin, Operation.Attributes.isLoopBegin])
        self.opcode = opcodes.opcodes.BeginDoWhile

class EndDoWhile(Operation):
    def __init__(self, comparater):
        super(EndDoWhile, self).__init__(numInputs=2, numOutputs=0, numTempvars=0, attributes=[Operation.Attributes.isBlockEnd, Operation.Attributes.isLoopEnd])
        self.opcode = opcodes.opcodes.EndDoWhile
        self.comparater = comparater

class EndForEach(Operation):
    def __init__(self):
        super(EndForEach, self).__init__(numInputs=0, numOutputs=0, numTempvars=0)
        self.opcode = opcodes.opcodes.EndIf

class Return(Operation):
    def __init__(self):
        super(Return, self).__init__(numInputs=1, numOutputs=0, numTempvars=0)
        self.opcode = opcodes.opcodes.Return

class Break(Operation):
    def __init__(self):
        super(Break, self).__init__(numInputs=0, numOutputs=0, numTempvars=0)
        self.opcode = opcodes.opcodes.Break

class Continue(Operation):
    def __init__(self):
        super(Continue, self).__init__(numInputs=0, numOutputs=0, numTempvars=0)
        self.opcode = opcodes.opcodes.Continue

class UnaryOperation(Operation):
    def __init__(self, op):
        super(UnaryOperation, self).__init__(numInputs=1, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.UnaryOperation
        self.op = op

    def __str__(self):
        return "out0 = " + opcodes.opcodes.opcodeList[self.opcode] + " " + str(self.op) + " inp0"

class BinaryOperation(Operation):
    def __init__(self, op):
        super(BinaryOperation, self).__init__(numInputs=2, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.BinaryOperation
        self.op = op

    def __str__(self):
        return "out0 = " + opcodes.opcodes.opcodeList[self.opcode] + " inp0, " + str(self.op) + " ,inp1"


class Include(Operation):
    def __init__(self):
        super(Include, self).__init__(numInputs=1, numOutputs=0, numTempvars=0)
        self.opcode = opcodes.opcodes.Include

class Eval(Operation):
    def __init__(self, value):
        super(Eval, self).__init__(numInputs=1, numOutputs=0, numTempvars=0)
        self.opcode = opcodes.opcodes.Eval
        self.value = value


class Phi(Operation):
    def __init__(self):
        super(Phi, self).__init__(numInputs = 1, numOutputs = 1, numTempvars = 0)
        self.opcode = opcodes.opcodes.Phi

class Copy(Operation):
    def __init__(self):
        super(Copy, self).__init__(numInputs = 2, numOutputs = 0, numTempvars = 0)
        self.opcode = opcodes.opcodes.Copy

class BeginFunction(Operation):
    def __init__(self,signature):
        super(BeginFunction, self).__init__(numInputs = 0, numOutputs = 1, numTempvars = signature.numArgs, attributes = [Operation.Attributes.isBlockBegin])
        self.opcode = opcodes.opcodes.BeginFunction
        self.signature = signature

class EndFunction(Operation):
    def __init__(self):
        super(EndFunction, self).__init__(numInputs=0, numOutputs=0, numTempvars=0, attributes = [Operation.Attributes.isBlockEnd])
        self.opcode = opcodes.opcodes.EndFunction



class ThrowException(Operation):
    def __init__(self):
        super(ThrowException, self).__init__(numInputs = 1, numOutputs= 0, numTempvars = 0, attributes = [])
        self.opcode = opcodes.opcodes.ThrowException

class BeginTry(Operation):
    def __init__(self):
        super(BeginTry, self).__init__(numInputs= 0, numOutputs= 0, numTempvars = 0, attributes = [Operation.Attributes.isBlockBegin])
        self.opcode = opcodes.opcodes.BeginTry

class BeginCatch(Operation):
    def __init__(self):
        super(BeginCatch, self).__init__(numInputs = 0, numOutputs= 0, numTempvars = 0, attributes = [Operation.Attributes.isBlockBegin, Operation.Attributes.isBlockEnd])
        self.opcode = opcodes.opcodes.BeginCatch

class EndTryCatch(Operation):
    def __init__(self):
        super(EndTryCatch, self).__init__(numInputs = 0, numOutputs= 0, numTempvars = 0, attributes = [Operation.Attributes.isBlockEnd])
        self.opcode = opcodes.opcodes.EndTryCatch

class CreateDict(Operation):
    def __init__(self, numInitialValues):
        super(CreateDict, self).__init__(numInputs=numInitialValues, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.CreateDict

class GetArrayElem(Operation):
    def __init__(self):
        super(GetArrayElem, self).__init__(numInputs=2, numOutputs=1, numTempvars=0)
        self.opcode = opcodes.opcodes.GetArrayElem

class SetArrayElem(Operation):
    def __init__(self):
        super(SetArrayElem, self).__init__(numInputs=3, numOutputs=0, numTempvars=0)
        self.opcode = opcodes.opcodes.SetArrayElem

class BeginClass(Operation):
    pass

class EndClass(Operation):
    pass

class BeginForEach(Operation):
    pass

class Print(Operation):
    def __init__(self):
        super(Print, self).__init__(numInputs = 1, numOutputs= 0, numTempvars = 0, attributes = [])
        self.opcode = opcodes.opcodes.Print

class Comparater:
    equal               = "=="
    strictEqual         = "==="
    notEqual            = "!="
    lessThan            = "<"
    lessThanOrEqual     = "<="
    greaterThan         = ">"
    greaterThanOrEqual  = ">="
    @staticmethod
    def all():
        return [Comparater.equal, Comparater.strictEqual, Comparater.notEqual, Comparater.lessThan, Comparater.lessThanOrEqual, Comparater.greaterThan, Comparater.greaterThanOrEqual]

class UnaryOperator:
    Inc         = "++"
    Dec         = "--"
    LogicalNot  = "!"
    BitwiseNot  = "~"

    @staticmethod
    def all():
        return [UnaryOperator.Inc, UnaryOperator.Dec, UnaryOperator.BitwiseNot, UnaryOperator.LogicalNot]


class BinaryOperator:
    Add     = "+"
    Sub     = "-"
    Mul     = "*"
    Div     = "/"
    Mod     = "%"
    BitAnd  = "&"
    BitOr   = "|"
    LogicAnd= "&&"
    LogicOr = "||"
    Xor     = "^"
    LShift  = "<<"
    RShift  = ">>"

    @staticmethod
    def all():
        return [BinaryOperator.Add, BinaryOperator.Sub, BinaryOperator.Mul, BinaryOperator.Div, BinaryOperator.Mod, BinaryOperator.BitAnd, BinaryOperator.BitOr, BinaryOperator.LogicAnd, BinaryOperator.LogicOr, BinaryOperator.Xor, BinaryOperator.LShift, BinaryOperator.RShift ]
