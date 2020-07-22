import operation
import variable
import opcodes

class Instruction:

    def __init__(self, operation, inputs=False, outputs=False, temp=False):
        self.operation = operation
        if inputs == False:
            self.inputs = []
        else:
            self.inputs = inputs

        if outputs == False:
            self.outputs = []
        else:
            self.outputs = outputs

        if temp == False:
            self.temp = []
        else:
            self.temp = temp

    def __str__(self):

        string = str(self.operation)

        inps = ""
        for i, val in enumerate(self.inputs):
            string = string.replace("inp"+str(i), str(val))

        for i, val in enumerate(self.outputs):
            string = string.replace("out"+str(i), str(val))

        return string

    '''getter for the ith input/output variable'''
    def getOutput(self,idx=0):
        return self.outputs[idx]

    def getInput(self,idx=0):
        return self.inputs[idx]

    def getTemp(self, idx=0):
        return self.temp[idx]

    '''getter for all output variable'''
    def getAllOutputs(self):
        return self.outputs

    def getAllInputs(self):
        return self.inputs

    def getAllTemps(self):
        return self.temp

    '''misc functions'''
    def isBeginFunction(self):
        return self.operation.opcode == opcodes.opcodes.BeginFunction

    def isEndFunction(self):
        return self.operation.opcode == opcodes.opcodes.EndFunction

    def isBeginElse(self):
        return self.operation.opcode == opcodes.opcodes.BeginElse

    def hasOutputs(self):
        return self.operation.numOutputs != 0

    def hasInputs(self):
        return self.operation.numInputs != 0

    def getOpcode(self):
        return self.operation.opcode


    '''Flag operations'''
    def isBlockBegin(self):
        return self.operation.getFlags() & self.operation.Attributes.isBlockBegin

    def isBlockEnd(self):
        return self.operation.getFlags() & self.operation.Attributes.isBlockEnd

    def isLoopBegin(self):
        return self.operation.getFlags() & operation.Operation.Attributes.isLoopBegin

    def isLoopEnd(self):
        return self.operation.getFlags() & operation.Operation.Attributes.isLoopEnd



if __name__ == '__main__':
    '''Tests'''
    def main():
            print Instruction(operation.Nop())
            print Instruction(operation.LoadInteger(1),False,[variable.Variable(12)])
            print Instruction(operation.LoadFloat(1.1),False,[variable.Variable(11)])
            print Instruction(operation.LoadString('aaaa'),False,[variable.Variable(12)])
            print Instruction(operation.LoadBoolean(True),False,[variable.Variable(12)])
            print Instruction(operation.LoadNull(),False,[variable.Variable(12)])
            print Instruction(operation.CreateArray(3),[variable.Variable(2),variable.Variable(3),variable.Variable(4)],[variable.Variable(12)])
            print Instruction(operation.CallFunction(2),[variable.Variable(1), variable.Variable(2), variable.Variable(3)], [variable.Variable(4)])
            #print Instruction(operation.CreateObject('blag', 3),[variable.Variable(1),variable.Variable(3),variable.Variable(2) ],[variable.Variable(12)]) //Error
            #print Instruction(operation.BeginFunction(),False,[variable.Variable(12)]) //NotCompleted
            #print Instruction(operation.EndFunction(),False,False) //NotCompleted
            print Instruction(operation.BeginIf(),[variable.Variable(1)],False)
            print Instruction(operation.BeginElse(),False,False)
            print Instruction(operation.EndIf(),False,False)
            print Instruction(operation.BeginWhile(">"),[variable.Variable(5), variable.Variable(0)],False) # Error
            print Instruction(operation.EndWhile(),False,False)
            print Instruction(operation.BeginFor("++", "<"),[variable.Variable(1), variable.Variable(4), variable.Variable(10)],False)
            print Instruction(operation.EndFor(),False,False)
            #print Instruction(operation.BeginForEach(),False,False) //NotCompleted
            #print Instruction(operation.EndForEach(),False,False) //NotCompleted
            print Instruction(operation.Return(),False,[variable.Variable(12)])
            print Instruction(operation.Break(),False,False)
            print Instruction(operation.Continue(),False,False)
            #print Instruction(operation.BeginTry(),False,False) //NotCompleted
            #print Instruction(operation.BeginCatch(),False,False) //NotCompleted
            #print Instruction(operation.EndTryCatch(),False,False) //NotCompleted
            #print Instruction(operation.BeginClass(),False,False) //NotMade
            #print Instruction(operation.EndClass(),False,False) //NotMade
            print Instruction(operation.UnaryOperation("++"),[variable.Variable(11)],[variable.Variable(10)])
            print Instruction(operation.BinaryOperation("+"),[variable.Variable(10), variable.Variable(11)],[variable.Variable(10)])
            print Instruction(operation.Include(),[variable.Variable("module")],False)
            print Instruction(operation.Eval('1'),[variable.Variable(11)],False)
            print Instruction(operation.Phi(), [variable.Variable(10)], [variable.Variable(12)])
            print Instruction(operation.Copy(), [variable.Variable(10), variable.Variable(20)], False)
            print Instruction(operation.ThrowException(), [variable.Variable(10)], False)
            print Instruction(operation.BeginTry(), False, False)
            print Instruction(operation.Copy(),False, [variable.Variable(20)])
            print Instruction(operation.Print(), [variable.Variable(10)], False)
            print Instruction(operation.BeginDoWhile(), False, False)
            print Instruction(operation.EndDoWhile(">"), [variable.Variable(1), variable.Variable(2)], False)

    #def tests():
    #    a = Instruction(operation.BeginWhile(">"),[variable.Variable(5), variable.Variable(0)],False)
    #    print a.isBeginFunction()

    #tests()


    main()
