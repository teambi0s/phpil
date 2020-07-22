class CodeEmitter:

    def __init__(self):
        self.code = ""
        self.indentLevel = 0

    def emit(self, text):
        self.code += "   "*self.indentLevel + text + "\n"

    def emitline(self, line):
        self.emit(line + ";")

    def increaseIndentLevel(self):
        self.indentLevel += 1

    def decreaseIndentLevel(self):
        self.indentLevel -= 1

    def getCode(self):
        return "<?php\n"+self.code+"\necho \"Done\";\n?>"

    def __str__(self):
        return self.getCode()
