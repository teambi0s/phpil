import opcodes

class Program:

    def __init__(self, *args):
        self.nextVariable = 0
        if len(args) == 0:
            self.instructionList = []
        elif len(args) == 1:
            self.instructionList = args[0]

    def append(self, instruction):
        # print instruction
        self.instructionList.append(instruction)

    def __str__(self):
        string = ""
        indentLevel = 0
        for i, ins in enumerate(self.instructionList):

            if ins.isBlockEnd() or ins.operation.opcode == opcodes.opcodes.BeginElse:
                indentLevel -= 1
            string += (str(i) + ": ").ljust(5,' ') + "\t"*indentLevel + str(ins) + "\n"
            if ins.isBlockBegin():
                indentLevel += 1

        return string

if __name__ == '__main__':
    import opcodes
    import operation
    import variable
    import instructions
    import typesData

    Program([
        instructions.Instruction(operation.Nop()), instructions.Instruction(operation.LoadInteger(1),False,[variable.Variable(12)])
    ])

    Program([
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
    ])

    print Program([
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
        instructions.Instruction(operation.EndFor(), False, False)

    ])

    Program()
    Program([
        instructions.Instruction(operation.LoadInteger(1),False,[variable.Variable(0)]),
        instructions.Instruction(operation.BeginFunction(typesData.FunctionSignature(2)),False,[variable.Variable(1)],[variable.Variable(10),variable.Variable(11)]),
        instructions.Instruction(operation.BinaryOperation("+"),[variable.Variable(10),variable.Variable(11)],[variable.Variable(2)]),
        instructions.Instruction(operation.LoadString("somestring"),False,[variable.Variable(3)]),
        instructions.Instruction(operation.Return(),[variable.Variable(3)]),
        instructions.Instruction(operation.EndFunction()),
        instructions.Instruction(operation.LoadInteger(1337),False,[variable.Variable(4)]),
        instructions.Instruction(operation.CallFunction(2),[variable.Variable(1), variable.Variable(4), variable.Variable(0)],[variable.Variable(6)]),
        instructions.Instruction(operation.LoadInteger(1337),False,[variable.Variable(7)]),
    ])



    # print Program([Instruction()])
