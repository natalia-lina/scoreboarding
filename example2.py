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
from system_state import SystemState
from stages import issue, read, execution, write

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

    register_status, instru_status, instru_stages = instantiate_registers_instructions_status(instru)
    fu_status = instantitate_functional_unit_status(fus)

    current_state = SystemState(instru, fus)
    future_state = current_state.copy()

    clock_cycle = 0
    future_state.clock_cycle = 1

    while clock_cycle<10:
        for idx, instru_stage in enumerate(current_state.instruction_stages):
            if instru_stage.stage is None or (instru_stage.stage is Pipeline.ISSUE and instru_stage.wait):
                future_state = issue(
                    current_state,
                    future_state,
                    fus,
                    instru[idx],
                    idx
                )
                break
            elif instru_stage.stage is Pipeline.ISSUE or (instru_stage.stage is Pipeline.READ and instru_stage.wait):
                future_state = read(
                    current_state,
                    future_state,
                    instru[idx],
                    idx
                )
            elif instru_stage.stage is Pipeline.READ or (instru_stage.stage is Pipeline.EXECUTION and instru_stage.wait):
                future_state = execution(current_state, future_state, instru[idx], fus, idx)
            elif instru_stage.stage is Pipeline.EXECUTION or (instru_stage.stage is Pipeline.WRITE and instru_stage.wait):
                future_state = write(current_state, future_state, instru[idx], idx)
            elif instru_stage.stage is Pipeline.WRITE and not instru_stage.wait:
                future_state.instruction_stages[idx].stage = Pipeline.DONE

        clock_cycle += 1


        future_state.update_instruction_status()
        current_state = future_state.copy()
        future_state.clock_cycle+= 1


        print("\n#############",clock_cycle, "#############\n")
        current_state.show_fu_status()
        print("\n")
        current_state.show_register_status()
        print("\n")
        current_state.show_instru_stages()
        print("\n")
        current_state.show_instru_status()
        print("\n##########################\n")



