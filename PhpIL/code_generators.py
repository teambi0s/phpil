import program_builder
import typesData
import variable
import operation
import probability

class CodeGenerator:

    # def __init__(self, obj):
    # print "__init__"
    #     #Assigning the object of programBuilder
    #     programBuilder = obj;

    @staticmethod
    def integerLiteralGenerator(programBuilder):
        # print "integerLiteralGenerator"
        programBuilder.loadInteger(programBuilder.getInt())
        return True

    @staticmethod
    def floatLiteralGenerator(programBuilder):
        # print "floatLiteralGenerator"
        programBuilder.loadFloat(programBuilder.getFloat())
        return True

    @staticmethod
    def stringLiteralGenerator(programBuilder):
        # print "stringLiteralGenerator"
        programBuilder.loadString(programBuilder.getString())
        return True

    @staticmethod
    def booleanLiteralGenerator(programBuilder):
        # print "booleanLiteralGenerator"
        programBuilder.loadBoolean(probability.Random.randomBool())
        return True

    @staticmethod
    def nullValueGenerator(programBuilder):
        # print "nullValueGenerator"
        programBuilder.loadNull()
        return True

    @staticmethod
    def intArrayGenerator(programBuilder):
        # print "intArrayGenerator"
        initial = []
        for i in range(probability.Random.randomInt(0,10)):
            initial.append(probability.Random.randomInt(0,6))
        programBuilder.createArray(initial)
        return True


    @staticmethod
    def dictGenerator(programBuilder):
        # print "dictGenerator"
        initial = []
        for i in range(probability.Random.randomInt(0,10)):
            key = probability.Random.withEqualProbability(
                lambda: programBuilder.getInt(),
                lambda: programBuilder.getFloat(),
                lambda: programBuilder.randVar(),
            )

            value = probability.Random.withEqualProbability(
                lambda: programBuilder.getInt(),
                lambda: programBuilder.getFloat(),
                lambda: programBuilder.randVar(),
            )

            initial.append((key,value))

        programBuilder.createDict(initial)
        return True

    @staticmethod
    def floatArrayGenerator(programBuilder):
        # print "floatArrayGenerator"
        initial = []
        for i in range(probability.Random.randomInt(0,10)):
            initial.append(probability.Random.randomFloat(0,6))
        programBuilder.createArray(initial)
        return True

    @staticmethod
    def unaryOperationGenerator(programBuilder):
        # print "unaryOperationGenerator"
        input = programBuilder.randVar(type = (typesData.Types.Integer) )
        programBuilder.unaryOperation(probability.Random.chooseUniform(operation.UnaryOperator.all()),input )
        return True

    @staticmethod
    def binaryOperationGenerator(programBuilder):
        # print "binaryOperationGenerator"
        lhs = programBuilder.randVar()
        rhs = programBuilder.randVar()
        programBuilder.binaryOperation(lhs, rhs, probability.Random.chooseUniform(operation.BinaryOperator.all()))
        return True

    #Create phi function in program_builder.py
    @staticmethod
    def phiGenerator(programBuilder):
        # print "phiGenerator"
        programBuilder.phi(programBuilder.randVar())
        return True

    @staticmethod
    def whileLoopGenerator(programBuilder):
        # print "whileLoopGenerator"
        start = programBuilder.loadInteger(0)
        end = programBuilder.loadInteger(probability.Random.randomInt(0,10))
        loopVar = programBuilder.phi(start)
        programBuilder.beginWhile(loopVar, "<", end)
        programBuilder.unaryOperation("++", loopVar)
        programBuilder.generateRandomInst()
        programBuilder.endWhile()

        return True


    @staticmethod
    def doWhileLoopGenerator(programBuilder):
        start = programBuilder.loadInteger(0)
        end = programBuilder.loadInteger(probability.Random.randomInt(0,10))
        loopVar = programBuilder.phi(start)
        programBuilder.beginDoWhile()
        programBuilder.unaryOperation("++", loopVar)
        programBuilder.generateRandomInst()
        programBuilder.endDoWhile(loopVar, "<", end)

    @staticmethod
    def ifStatementGenerator(programBuilder):
        # print "ifStatementGenerator"
        cond = programBuilder.randVar(type=typesData.Types.Boolean)
        a = programBuilder.randVar()
        phi = programBuilder.phi(a)
        programBuilder.beginIf(cond)
        programBuilder.generateRandomInst()
        programBuilder.copy(phi, programBuilder.randVar())
        programBuilder.beginElse()
        programBuilder.generateRandomInst()
        programBuilder.copy(phi, programBuilder.randVar())
        programBuilder.endIf()

        return True


    @staticmethod
    def forLoopGenerator(programBuilder):
        # print "forLoopGenerator"
        start = programBuilder.loadInteger(0)
        end = programBuilder.loadInteger(probability.Random.randomInt(0,10))
        # programBuilder.binaryOperation()
        step = programBuilder.loadInteger(1)
        programBuilder.beginFor(start, "<", end, "+", step)
        programBuilder.generateRandomInst()
        programBuilder.endFor()


    @staticmethod
    def breakGenerator(programBuilder):
        # print "breakGenerator"
        if programBuilder.lastContextisLoop():
            programBuilder.doBreak()
            return True
        return False


    @staticmethod
    def continueGenerator(programBuilder):
        # print "continueGenerator"
        if programBuilder.lastContextisLoop():
            programBuilder.doContinue()
            return True
        return False

    @staticmethod
    def functionDefinationGenerator(programBuilder):
        # print "functionDefinationGenerator"
        visbleVars = programBuilder.getVisibleVars()
        usableVars = []
        for i in visbleVars:
            if programBuilder.typeAnalyzer.getType(i) == typesData.Types.Function and programBuilder.typeAnalyzer.getSignature(i).isConstructing():
                continue
            usableVars.append(i)
        signature = typesData.FunctionSignature(probability.Random.randomInt(1,5), usableVars)
        function = programBuilder.functionDefination(signature)
        programBuilder.generateRandomInst()
        returnValue = programBuilder.randVar()
        CodeGenerator.functionReturnGenerator(programBuilder)
        programBuilder.endFunction()


        # programBuilder.generateRandomInst()
        programBuilder.generateRandomInst()
        arguments = programBuilder.generateCallArguments(function)
        if not isinstance(arguments, list):
            return False
        programBuilder.callFunction(function, arguments)

        return True

    @staticmethod
    def functionReturnGenerator(programBuilder):
        # print "functionReturnGenerator"
        if programBuilder.isInFunction():
            programBuilder.doReturn(programBuilder.randVar())
            return True
        return False

    @staticmethod
    def functionCallGenerator(programBuilder):
        # print "functionCallGenerator"
        function = programBuilder.randVar(type = typesData.Types.Function)
        if not isinstance(function, variable.Variable):
            return False
        # recursive = programBuilder.checkRecursion(function)
        # if recursive:
        #     return False
        arguments = programBuilder.generateCallArguments(function)
        if not isinstance(arguments, list):
            return False
        programBuilder.callFunction(function, arguments)
        return True

    @staticmethod
    def tryCatchGenerator(programBuilder):
        # print "tryCatchGenerator"
        v = programBuilder.phi(programBuilder.randVar())
        programBuilder.beginTry()
        programBuilder.generateRandomInst()
        programBuilder.copy(programBuilder.randVar(), v)
        programBuilder.beginCatch()
        # programBuilder.generateRandomInst()
        programBuilder.copy(programBuilder.randVar(), v)
        programBuilder.endTryCatch()

    @staticmethod
    def throwGenerator(programBuilder):
        # print "throwGenerator"
        v = programBuilder.randVar()
        programBuilder.throwException(v)

    @staticmethod
    def arrayLiteralGenerator(programBuilder):
        # print "arrayLiteralGenerator"
        initial = []
        for i in range(probability.Random.randomInt(0,6)):
            initial.append(programBuilder.randVar())
        programBuilder.createArray(initial)
        return True

    @staticmethod
    def getArrayElemGenerator(programBuilder):
        # print "getArrayElemGenerator"
        arr = programBuilder.randVar(type = typesData.Types.Array)
        if not arr:
            arr = programBuilder.randVar(type = typesData.Types.String)

        lst = range(probability.Random.randomInt(0,10))
        temp = programBuilder.getInt()
        lst.append(temp)
        index = probability.Random.chooseUniform(lst)
        programBuilder.getArrayElem(arr, index)
        return True

    @staticmethod
    def setArrayElemGenerator(programBuilder):
        # print "setArrayElemGenerator"
        arr = programBuilder.randVar(type = typesData.Types.Array)
        if not arr:
            arr = programBuilder.randVar(type = typesData.Types.String)

        lst = range(probability.Random.randomInt(0,10))
        temp = programBuilder.getInt()
        lst.append(temp)
        index = probability.Random.chooseUniform(lst)
        value = programBuilder.randVar()
        programBuilder.setArrayElem(arr, index, value)
        return True


    #objectLiteralGenerator not created.
    #objectLiteralWithSpreadGenerator not created
    #builinGenerator not created
    #functionDefinationGenerator not created
    #propertyRetrievalGenerator not created
    #propertyAssignmentGenerator not created
    #propertyRemovalGenerator not created
    #elementRetrievalGenerator not created
    #elementAssignmentGenerator not created
    #elementRemovalGenerator not created
    #computedPropertyAssignmentGenerator not created
    #computedPropertyRetrievalGenerator not created
    #computedPropertyRemovalGenerator not created
    #typeTestGenerator not created
    #instanceOfGenerator not created
    #inGenerator not created
    #methodCallGenerator not created
    #functionCallGenerator not created
    #constructorCallGenerator not created
    #functionCallWithSpreadGenerator not created
    #reassignmentGenerator not created
    #comparisonGenerator not created
    #ifStatementGenerator not created ***
