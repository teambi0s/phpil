import code_generators

class Settings:

    allCodeGenerators = {
        code_generators.CodeGenerator.integerLiteralGenerator : 5,
        code_generators.CodeGenerator.floatLiteralGenerator : 2,
        code_generators.CodeGenerator.stringLiteralGenerator : 3,
        code_generators.CodeGenerator.booleanLiteralGenerator : 2,
        code_generators.CodeGenerator.nullValueGenerator : 2,
        code_generators.CodeGenerator.unaryOperationGenerator : 20,
        code_generators.CodeGenerator.binaryOperationGenerator : 20,
        code_generators.CodeGenerator.phiGenerator : 0,
        code_generators.CodeGenerator.whileLoopGenerator : 5,
        code_generators.CodeGenerator.ifStatementGenerator : 20,
        code_generators.CodeGenerator.forLoopGenerator : 15,
        code_generators.CodeGenerator.breakGenerator : 20,
        code_generators.CodeGenerator.continueGenerator : 20,
        code_generators.CodeGenerator.functionDefinationGenerator : 30,
        code_generators.CodeGenerator.functionReturnGenerator : 0,
        code_generators.CodeGenerator.functionCallGenerator : 80,
        code_generators.CodeGenerator.tryCatchGenerator : 1,
        code_generators.CodeGenerator.throwGenerator : 0,
        code_generators.CodeGenerator.floatArrayGenerator : 20,
        code_generators.CodeGenerator.intArrayGenerator : 20,
        code_generators.CodeGenerator.arrayLiteralGenerator : 20,
        code_generators.CodeGenerator.doWhileLoopGenerator : 5,
        code_generators.CodeGenerator.dictGenerator: 10,
        code_generators.CodeGenerator.getArrayElemGenerator: 20,
        code_generators.CodeGenerator.setArrayElemGenerator: 20
    }
