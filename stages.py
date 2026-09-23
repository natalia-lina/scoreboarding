from basics import (
    Instruction,
    InstructionStage,
    FunctionalUnitStatus,
    RegisterStatus,
    Pipeline
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
    future_state.instru_stages[idx].stage = Pipeline.ISSUE
    
    if current_state.register_status[instruction.fi].fu is not None:
        future_state.instru_stages[idx].wait = True
        return future_state
    
    for name, fu in functional_units.items():
        if fu.kind == MAPPING[instruction.op] and not current_state.fu_status[name].busy:
            future_state.fu_status[name].busy = True
            future_state.fu_status[name].op = instruction.op
            future_state.fu_status[name].fi = instruction.fi
            future_state.fu_status[name].fj = instruction.fj
            future_state.fu_status[name].fk = instruction.fk

            future_state.fu_status[name].qj = current_state.register_status[instruction.fj].fu

            if instruction.fk is not None:
                future_state.fu_status[name].qk = current_state.register_status[instruction.fk].fu

            future_state.fu_status[name].rj = future_state.fu_status[name].qj is None
            future_state.fu_status[name].rk = future_state.fu_status[name].qk is None

            future_state.register_status[instruction.fi].fu = name

            future_state.instru_stages[idx].wait = False
            return future_state

    future_state.instru_stages[idx].wait = True
    return future_state

def read(
    current_state: SystemState,
    future_state: SystemState,
    instruction: Instruction,
    idx: int # instruction index
):
    future_state.instru_stages[idx].stage = Pipeline.READ
    fu_name = current_state.register_status[instruction.fi].fu

    if current_state.fu_status[fu_name].rj and current_state.fu_status[fu_name].rk:
        future_state.fu_status[fu_name].rj = False
        future_state.fu_status[fu_name].rk = False
        future_state.instru_stages[idx].wait = False
        return future_state
    
    future_state.instru_stages[idx].wait = True
    return future_state

def execution(
    current_state: SystemState,
    future_state: SystemState,
    instruction: Instruction,
    functional_units: dict,
    idx
):
    future_state.instru_stages[idx].stage = Pipeline.EXECUTION
    fu_name = current_state.register_status[instruction.fi].fu
    if current_state.instru_status[idx].read is None:
        future_state.instru_stages[idx].wait = True
    elif functional_units[fu_name].latency > current_state.clock_cycle-current_state.instru_status[idx].read:
        future_state.instru_stages[idx].wait = True
    else:
        future_state.instru_stages[idx].wait = False
    return future_state
