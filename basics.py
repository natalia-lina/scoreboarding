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
        self.wait = False

    def issue(self, fus, fu_status, reg_status):
        self.stage = Pipeline.ISSUE

        if reg_status[self.fi].fu is not None:
            self.wait = True
            return fu_status, reg_status
        
        for name, fu in fus.items():
            if fu.kind == MAPPING[self.op] and not fu_status[name].busy:

                fu_status[name].busy = True
                fu_status[name].op = self.op
                fu_status[name].fi = self.fi
                fu_status[name].fj = self.fj
                fu_status[name].fk = self.fk

                fu_status[name].qj = reg_status[self.fj].fu

                if self.fk is not None:
                    fu_status[name].qk = reg_status[self.fk].fu

                fu_status[name].rj = fu_status[name].qj is None
                fu_status[name].rk = fu_status[name].qk is None

                reg_status[self.fi].fu = name

                self.wait = False
                return fu_status, reg_status
        
        self.wait = True

    def read(self, fu_status, reg_status):
        self.stage = Pipeline.READ
        fu_name = reg_status[self.fi].fu

        if fu_status[fu_name].rj and fu_status[fu_name].rk:
            fu_status[fu_name].rj = False
            fu_status[fu_name].rk = False
            self.wait = False
            return fu_status

        self.wait = True
        return fu_status

    def complete(self, fus, reg_status, instru_status, current_cycle):
        self.stage = Pipeline.COMPLETE
        fu_name = reg_status[self.fi].fu
        if fus[fu_name].latency > current_cycle-instru_status.read:
            self.wait = True
        else:
            self.wait = False
        instru_status.complete = current_cycle
        return instru_status
    
    def write(self, reg_status, fu_status):
        self.stage = Pipeline.WRITE
        fu_name = reg_status[self.fi].fu
        for name, fu_s in fu_status.items():
            if fu_name == name:
                continue
            if fu_s.busy:
                if fu_s.fj == fu_status[fu_name].fi and fu_s.rj:
                    self.wait = True
                    return reg_status, fu_status

                if fu_s.fk == fu_status[fu_name].fi and fu_s.rk:
                    self.wait = True
                    return reg_status, fu_status
        
        for name, fu_s in fu_status.items():
            if name == fu_name:
                continue
            if fu_s.qj == fu_name:
                fu_s.qj = None
                fu_s.rj = True
            if fu_s.qk == fu_name:
                fu_s.qk = None
                fu_s.rk = True

            reg_status[self.fi].fu = None
            fu_status[fu_name] = FunctionalUnitStatus()
        self.wait = False
        return reg_status, fu_status


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
