from PhpIL import program_builder
from PhpIL import program
from PhpIL import lifter

def main():
    pb = program_builder.ProgramBuilder()
    for i in range(4):
        pb.generateRandomInst()

    prog = pb.finish()

    lift = lifter.Lifter(prog)
    lift.doLifting()
    code = lift.getCode()
    print code

if __name__ == '__main__':
    main()
