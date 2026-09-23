from basics import (
    Instruction, Load, Store, FunctionalUnit,
    RegisterStatus, FunctionalUnitStatus, InstructionStatus, Pipeline
)

from utils import (
    load_instructions,
    load_configurations,
    instantiate_registers_instructions_status,
    instantitate_functional_unit_status
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


if __name__ == "__main__":

    fus=load_configurations(CONFIGURATIONS)
    instru=load_instructions(INSTRUCTIONS)

    register_status, instru_status = instantiate_registers_instructions_status(instru)
    fu_status = instantitate_functional_unit_status()

    ######### Clock 0 #############

    n_inst = len(instru)
    clock = 1

    prev_fu_status, prev_register_status = fu_status, register_status

    while clock<6:
        print(f"######## CLOCK = {clock} ########\n")

        print(InstructionStatus.__name__)
        for idx, status in enumerate(instru_status):
            if idx < clock:
                # Se a instrução ainda não foi iniciada ou está na etapa de issue e em stall, executar etapa issue
                if instru[idx].stage is None or (instru[idx].stage is Pipeline.ISSUE and instru[idx].wait):
                    fu_status, register_status = instru[idx].issue(fus, prev_fu_status, prev_register_status)
                    instru_status[idx].issue = clock
                
                # Se a instrução está na etapa de issue e não está em stall, executar leitura de operandos
                elif (instru[idx].stage is Pipeline.ISSUE and not instru[idx].wait) or (instru[idx].stage is Pipeline.READ and instru[idx].wait):
                    fu_status = instru[idx].read(prev_fu_status, prev_register_status)
                    instru_status[idx].read = clock

                # Se a instrução está na etapa de read e não está em stall ou está na etapa complete e ainda não "esperou" a latencia
                elif (instru[idx].stage is Pipeline.READ and not instru[idx].wait) or (instru[idx].stage is Pipeline.COMPLETE and instru[idx].wait):
                    instru_status[idx] = instru[idx].complete(fus, prev_register_status, instru_status[idx], clock)
                
                elif (instru[idx].stage is Pipeline.COMPLETE and not instru[idx].wait) or (instru[idx].stage is Pipeline.WRITE and instru[idx].wait):
                    register_status, fu_status = instru[idx].write(prev_register_status, prev_fu_status)
                    instru_status[idx].write = clock

        for idx, status in enumerate(instru_status):
            print(f"I{idx+1}", status.__dict__)

        print("\n", FunctionalUnitStatus.__name__)
        for name, status in fu_status.items():
            print(name, status.__dict__)

        print("\n", FunctionalUnitStatus.__name__)
        for name, status in prev_fu_status.items():
            print(name, status.__dict__)

        print("\n", RegisterStatus.__name__)
        for reg, status in register_status.items():
            print(reg, status.fu)

        print("\n", RegisterStatus.__name__)
        for reg, status in prev_register_status.items():
            print(reg, status.fu)
        
        clock+=1
        prev_fu_status, prev_register_status = fu_status, prev_register_status
        print("\n")


