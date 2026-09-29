from enum import Enum

MAPPING = {
    "fld": "int",
    "fsd": "int",
    "fadd": "add",
    "fsub": "add",
    "fmul": "mult",
    "fdiv": "div"
}

class Stage(Enum):
    ISSUE = 1
    READ = 2
    EXECUTION = 3
    WRITE = 4
    DONE = 5


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
    def __init__(self, components: list[str | None]):
        self.op = components[0]
        self.fk = None
        self.__instantiate_registers(components[1:])

    def __instantiate_registers(self, registers: list[str | None]):
        if self.op == "fld":
            self.fi = self.__parse_register(registers[0])
            self.fj = self.__parse_register(registers[1])
        elif self.op == "fsd":
            self.fi = self.__parse_register(registers[1])
            self.fj = self.__parse_register(registers[0])
        else:
            self.fi = self.__parse_register(registers[0])
            self.fj = self.__parse_register(registers[1])
            self.fk = self.__parse_register(registers[2])          


    def __parse_register(self, reg: str):
        return reg.split("(")[-1].replace(")", "")


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
        self.qi = None

    def copy(self):
        cp = RegisterStatus()
        cp.qi = self.qi
        return cp
