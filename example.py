from basics import (
    Instruction, Load, Store, FunctionalUnit,
    RegisterStatus, FunctionalUnitStatus, InstructionStatus, Pipeline
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

    fus = {}
    for line in lines:
        components = line.split(" ")
        kind = components[0]
        num = int(components[1])
        lat = int(components[2])

        fu = FunctionalUnit(kind, lat)

        for idx in range(num):
            fus[f"{kind}{idx+1}"] = fu
    
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

        instru_status.append(InstructionStatus())

    fu_status = {}
    for name, fu in fus.items():
        fu_status[name]=FunctionalUnitStatus()

    ######### Clock 0 #############

    n_inst = len(instru)
    clock = 1

    while clock<n_inst+5:
        print(f"######## CLOCK = {clock} ########\n")

        print(InstructionStatus.__name__)
        for idx, status in enumerate(instru_status):
            if idx < clock:
                # Se a instrução ainda não foi iniciada ou está na etapa de issue e em stall, executar etapa issue
                if instru[idx].stage is None or (instru[idx].stage is Pipeline.ISSUE and instru[idx].wait):
                    fu_status, reg_status = instru[idx].issue(fus, fu_status, register_status)
                    instru_status[idx].issue = clock
                
                # Se a instrução está na etapa de issue e não está em stall, executar leitura de operandos
                elif (instru[idx].stage is Pipeline.ISSUE and not instru[idx].wait) or (instru[idx].stage is Pipeline.READ and instru[idx].wait):
                    fu_status = instru[idx].read(fu_status, register_status)
                    instru_status[idx].read = clock

                elif (instru[idx].stage is Pipeline.READ and not instru[idx].wait) or (instru[idx].stage is Pipeline.COMPLETE and instru[idx].wait):
                    instru_status[idx] = instru[idx].complete(fus, reg_status, instru_status[idx], clock)


        for idx, status in enumerate(instru_status):
            print(f"I{idx+1}", status.__dict__)

        print("\n", FunctionalUnitStatus.__name__)
        for name, status in fu_status.items():
            print(name, status.__dict__)

        print("\n", RegisterStatus.__name__)
        for reg, status in register_status.items():
            print(reg, status.fu)
        
        clock+=1
        print("\n")


