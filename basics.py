from enum import Enum

MAPPING = {
    "fld": "int",
    "fsd": "int",
    "fadd": "add",
    "fsub": "add",
    "fmul": "mul",
    "fdiv": "div"
}

class FunctionalUnit:
    def __init__(self, kind, latency):
        self.kind = kind
        self.latency = latency


class Instruction:
    def __init__(self, op, fi, fj, fk):
        self.op = op
        self.fi = fi
        self.fj = fj
        self.fk = fk
        self.stage = None

    def issue(self, fus, fu_status, reg_status):

        if reg_status[self.fi] is not None:
            return fu_status, reg_status
        
        for idx, fu in enumerate(fus):
            if fu.kind == MAPPING[self.op] and not fu_status[idx].busy:

                fu_status[idx].busy = True
                fu_status[idx].op = self.op
                fu_status[idx].fi = self.fi
                fu_status[idx].fj = self.fj
                fu_status[idx].fk = self.fk

                fu_status[idx].qj = reg_status[self.fj]
                fu_status[idx].qk = reg_status[self.fk]

                fu_status[idx].rj = fu_status[idx].qj is None
                fu_status[idx].rk = fu_status[idx].qk is None

                reg_status[self.fi] = idx

                return fu_status, reg_status

    def read(self, fu_status):
        for fu_s in fu_status:
            if fu_s.fk == self.fk and fu_s.fj == self.fj and fu_s.fi == self.fi and fu_s.op == self.op:
                if fu_s.rj and fu_s.rk:
                    fu_s.rj = False
                    fu_s.rk = False
                    return fu_status
        return fu_status


class Load(Instruction):
    def __init__(self, fi, fj):
        super().__init__("fld", fi, fj, None)


class Store(Instruction):
    def __init__(self, fi, fj):
        super().__init__("fsd", fi, fj,  None)


class Pipeline(Enum):
    ISSUE = 1
    READ = 2
    COMPLETE = 3
    WRITE = 4


class InstructionStatus:
    def __init__(self):
        self.issue = None
        self.read = None
        self.complete = None
        self.write = None


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


class RegisterStatus:
    def __init__(self):
        self.fu = None
