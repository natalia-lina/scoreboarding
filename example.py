from basics import (
    Instruction, Load, Store, FunctionalUnit,
    RegisterStatus, FunctionalUnitStatus, InstructionStatus
)

INSTRUCTIONS = """fld f1, 0(x1)
fsd f5, 0(x1)
fdiv f2, f4, f5
"""

CONFIGURATIONS = """int 2 1
mul 2 4
add 1 2
div 1 10
"""

def load_instructions():
    lines = INSTRUCTIONS.splitlines()

    instant = []

    for line in lines:
        components = line.replace(",", "").split(" ")
        op = components[0]

        if op == "fld":
            instant.append(Load(*components[1:]))
        
        elif op == "fsd":
            instant.append(Store(*components[1:]))
        
        else:
            instant.append(Instruction(*components))

    return instant


def load_configurations():
    lines = CONFIGURATIONS.splitlines()

    fus = []
    for line in lines:
        components = line.split(" ")
        kind = components[0]
        num = int(components[1])
        lat = int(components[2])

        fu = FunctionalUnit(kind, lat)

        for _ in range(num):
            fus.append(fu)
    
    return fus

if __name__ == "__main__":

    fus=load_configurations()
    instru=load_instructions()

    register_status = {}
    instru_status = []
    for ins in instru:
        if ins.fi is not None:
            register_status[ins.fi] = RegisterStatus()
        if ins.fj is not None:
            register_status[ins.fj] = RegisterStatus()
        if ins.fk is not None:
            register_status[ins.fk] = RegisterStatus()

        instru_status.append(InstructionStatus)

    fu_status = []
    for fu in config:
        fu_status.append(FunctionalUnitStatus())

    print(instru_status)
    print(register_status)
    print(fu_status)

    ######### Clock 0 #############


