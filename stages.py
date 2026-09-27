from enum import Enum
from basics import (
    Instruction,
    InstructionStage,
    FunctionalUnitStatus,
    RegisterStatus,
    Stage
)

from system_state import SystemState

MAPPING = {
    "fld": "int",
    "fsd": "int",
    "fadd": "add",
    "fsub": "add",
    "fmul": "mul",
    "fdiv": "div"
}

def issue(
    current_state: SystemState,
    future_state: SystemState,
    functional_units: dict,
    instruction: Instruction,
    idx: int # instruction index
):
    future_state.instruction_stages[idx].stage = Stage.ISSUE
    
    if current_state.register_status[instruction.fi].qi is not None:
        future_state.instruction_stages[idx].wait = True
        return future_state
    
    for name, fu in functional_units.items():
        if fu.kind == MAPPING[instruction.op] and not current_state.functional_unit_status[name].busy:
            future_state.functional_unit_status[name].busy = True
            future_state.functional_unit_status[name].op = instruction.op
            future_state.functional_unit_status[name].fi = instruction.fi
            future_state.functional_unit_status[name].fj = instruction.fj
            future_state.functional_unit_status[name].fk = instruction.fk

            future_state.functional_unit_status[name].qj = current_state.register_status[instruction.fj].qi

            if instruction.fk is not None:
                future_state.functional_unit_status[name].qk = current_state.register_status[instruction.fk].qi

            future_state.functional_unit_status[name].rj = future_state.functional_unit_status[name].qj is None
            future_state.functional_unit_status[name].rk = future_state.functional_unit_status[name].qk is None

            future_state.register_status[instruction.fi].qi = name

            future_state.instruction_stages[idx].wait = False
            return future_state

    future_state.instruction_stages[idx].wait = True
    return future_state

def read(
    current_state: SystemState,
    future_state: SystemState,
    instruction: Instruction,
    idx: int # instruction index
):
    future_state.instruction_stages[idx].stage = Stage.READ
    fu_name = current_state.register_status[instruction.fi].qi
    if current_state.functional_unit_status[fu_name].rj and current_state.functional_unit_status[fu_name].rk:
        future_state.functional_unit_status[fu_name].rj = False
        future_state.functional_unit_status[fu_name].rk = False
        future_state.instruction_stages[idx].wait = False
        return future_state
    
    future_state.instruction_stages[idx].wait = True
        
        
    return future_state

def execution(
    current_state: SystemState,
    future_state: SystemState,
    instruction: Instruction,
    functional_units: dict,
    idx
):
    future_state.instruction_stages[idx].stage = Stage.EXECUTION
    fu_name = current_state.register_status[instruction.fi].qi

    if current_state.instruction_status[idx].read is None:
        future_state.instruction_stages[idx].wait = True
        return future_state
    elif functional_units[fu_name].latency-1 > current_state.clock_cycle-current_state.instruction_status[idx].read:
        future_state.instruction_stages[idx].wait = True
        return future_state
    
    future_state.instruction_stages[idx].wait = False
    return future_state

def write(current_state, future_state, instruction, idx):
    future_state.instruction_stages[idx].stage = Stage.WRITE
    fu_name = current_state.register_status[instruction.fi].qi
    for name, status in current_state.functional_unit_status.items():
        if name != fu_name and status.busy:
            if (status.fj == current_state.functional_unit_status[fu_name].fi and status.rj):
                future_state.instruction_stages[idx].wait = True
                return future_state
            if (status.fk == current_state.functional_unit_status[fu_name].fi and status.rk):
                future_state.instruction_stages[idx].wait = True
                return future_state
    if fu_name == "int2":
        print("1 #########")
        for name, fu in current_state.functional_unit_status.items():
            print(name, fu is future_state.functional_unit_status[name])
        # print(current_state.register_status is future_state.register_status)
        # current_state.show_fu_status()
        # current_state.show_register_status()
        # future_state.show_register_status() 
    for name, status in current_state.functional_unit_status.items():

        if status.qj == fu_name:
            future_state.functional_unit_status[name].qj = None
            future_state.functional_unit_status[name].rj = True

        if status.qk == fu_name:
            future_state.functional_unit_status[name].qk = None
            future_state.functional_unit_status[name].rk = True
    # if fu_name == "int2":
    #     print("2 #########")
        # current_state.show_fu_status()
        # current_state.show_register_status()
        # future_state.show_register_status()

    if current_state.register_status[current_state.functional_unit_status[fu_name].fi].qi == fu_name:
        # print(idx,current_state.functional_unit_status[fu_name].fi)
        future_state.register_status[current_state.functional_unit_status[fu_name].fi].qi = None
        current_state.show_register_status()



    future_state.functional_unit_status[fu_name] = FunctionalUnitStatus()
    future_state.instruction_stages[idx].wait = False


    return future_state
