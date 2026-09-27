from enum import Enum

MAPPING = {
    "fld": "int",
    "fsd": "int",
    "fadd": "add",
    "fsub": "add",
    "fmul": "mul",
    "fdiv": "div"
}



class FunctionalUnitStatus:
    def __init__(self):

        self.busy = False
        self.op = None
        self.fi = None
        self.fj = None
        self.fk = None
        self.qj = None
        self.qk = None
        self.rj = None
        self.rk = None

    def copy(self):
        cp = FunctionalUnitStatus()
        cp.busy = self.busy
        cp.op = self.op
        cp.fi = self.fi
        cp.fj = self.fj
        cp.fk = self.fk
        cp.qj = self.qj
        cp.qk = self.qk
        cp.rj = self.rj
        cp.rk = self.rk
        return cp
        

class FunctionalUnit:
    def __init__(self, kind, latency):
        self.kind = kind
        self.latency = latency


class InstructionStatus:
    def __init__(self):
        self.issue = None
        self.read = None
        self.execution = None
        self.write = None

    def copy(self):
        cp = InstructionStatus()
        cp.issue = self.issue
        cp.read = self.read
        cp.execution = self.execution
        cp.write = self.write
        return cp


class Instruction:
    def __init__(self, op, fi, fj, fk):
        self.op = op
        self.fi = self.__parse_register(fi)
        self.fj = self.__parse_register(fj)
        self.fk = self.__parse_register(fk)

    def __parse_register(self, reg: str):
        if reg is None:
            return reg
        return reg.split("(")[-1].replace(")", "")


class Pipeline(Enum):
    ISSUE = 1
    READ = 2
    EXECUTION = 3
    WRITE = 4
    DONE = 5


class InstructionStage:
    def __init__(self):
        self.stage = None
        self.wait = False

    def copy(self):
        cp = InstructionStage()
        cp.stage = self.stage 
        cp.wait = self.wait
        return cp

class RegisterStatus:
    def __init__(self):
        self.fu = None

    def copy(self):
        cp = RegisterStatus()
        cp.fu = self.fu
        return cp
