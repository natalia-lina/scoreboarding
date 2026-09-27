from utils import load_inputs
from system_state import SystemState
from basics import Stage
from stages import issue, read, execution, write

if __name__ == "__main__":

    current_state = SystemState(*load_inputs("ex2.s", "config1"))
    future_state = current_state.copy()

    clock_cycle = 0
    future_state.clock_cycle = 1

    while not current_state.finished():

        for idx, instru_stage in enumerate(current_state.instruction_stages):
            if instru_stage.stage is None or (instru_stage.stage is Stage.ISSUE and instru_stage.wait):
                future_state = issue(
                    current_state,
                    future_state,
                    idx
                )
                break
            elif instru_stage.stage is Stage.ISSUE or (instru_stage.stage is Stage.READ and instru_stage.wait):
                future_state = read(
                    current_state,
                    future_state,
                    idx
                )
            elif instru_stage.stage is Stage.READ or (instru_stage.stage is Stage.EXECUTION and instru_stage.wait):
                future_state = execution(current_state, future_state, idx)
            elif instru_stage.stage is Stage.EXECUTION or (instru_stage.stage is Stage.WRITE and instru_stage.wait):
                future_state = write(current_state, future_state, idx)
            elif instru_stage.stage is Stage.WRITE and not instru_stage.wait:
                future_state.instruction_stages[idx].stage = Stage.DONE

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







