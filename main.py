from argparse import ArgumentParser
from utils import load_inputs
from system_state import SystemState
from basics import Stage
from stages import issue, read, execution, write

parser = ArgumentParser()
parser.add_argument("-p", "--program", required=True, help="Path to RISC-V assembly instructions file")
parser.add_argument("-c", "--configuration", required=True, help="Path to function unities configuration file")
parser.add_argument("-v", "--verbose", action="store_true", required=False, help="Use verbose option to print system state in each clock cycle")

if __name__ == "__main__":

    args = parser.parse_args()

    current_state = SystemState(*load_inputs(args.program, args.configuration))
    future_state = current_state.copy()

    clock_cycle = 0
    future_state.clock_cycle = 1

    while not current_state.finished():

        for idx, instru_stage in enumerate(current_state.instruction_stages):
            if instru_stage.stage is None or (instru_stage.stage is Stage.ISSUE and instru_stage.wait):
                future_state = issue(current_state, future_state, idx)
                break
            elif instru_stage.stage is Stage.ISSUE or (instru_stage.stage is Stage.READ and instru_stage.wait):
                future_state = read(current_state,future_state, idx)
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

        if args.verbose:

            print(f"\n\n\n############# {clock_cycle=} #############\n\n")
            current_state.show_fu_status()
            print("\n")
            current_state.show_register_status()
            print("\n")
            current_state.show_instru_status()

    if not args.verbose:
        current_state.show_instru_status()







