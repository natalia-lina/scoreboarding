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

class FunctionalUnit:
    def __init__(self, kind, latency):
        self.kind = kind
        self.latency = latency
        self.status = FunctionalUnitStatus()


class InstructionStatus:
    def __init__(self):
        self.issue = None
        self.read = None
        self.execution = None
        self.write = None

class Instruction:
    def __init__(self, op, fi, fj, fk):
        self.op = op
        self.fi = fi
        self.fj = fj
        self.fk = fk

class Load(Instruction):
    def __init__(self, fi, fj):
        super().__init__("fld", fi, fj, None)


class Store(Instruction):
    def __init__(self, fi, fj):
        super().__init__("fsd", fi, fj,  None)


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

class RegisterStatus:
    def __init__(self):
        self.fu = None


class Scoreboarding:
    def __init__(self, instructions, functional_units, registers):
        self.instructions = instructions
        self.functional_units = functional_units
        self.registers = registers