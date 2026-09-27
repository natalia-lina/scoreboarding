from basics import (
    MAPPING,
    FunctionalUnitStatus,
    Stage
)

from system_state import SystemState

def issue(
    current_state: SystemState,
    future_state: SystemState,
    idx: int # instruction index
):
    future_state.instruction_stages[idx].stage = Stage.ISSUE
    fu_exists = False
    
    if current_state.register_status[current_state.instructions[idx].fi].qi is not None:
        future_state.instruction_stages[idx].wait = True
        return future_state
    
    for name, fu in current_state.functional_units.items():
        if fu.kind == MAPPING[current_state.instructions[idx].op]:
            fu_exists = True
            if not current_state.functional_unit_status[name].busy:
                future_state.functional_unit_status[name].busy = True
                future_state.functional_unit_status[name].op = current_state.instructions[idx].op
                future_state.functional_unit_status[name].fi = current_state.instructions[idx].fi
                future_state.functional_unit_status[name].fj = current_state.instructions[idx].fj
                future_state.functional_unit_status[name].fk = current_state.instructions[idx].fk

                future_state.functional_unit_status[name].qj = current_state.register_status[current_state.instructions[idx].fj].qi

                if current_state.instructions[idx].fk is not None:
                    future_state.functional_unit_status[name].qk = current_state.register_status[current_state.instructions[idx].fk].qi

                future_state.functional_unit_status[name].rj = future_state.functional_unit_status[name].qj is None
                future_state.functional_unit_status[name].rk = future_state.functional_unit_status[name].qk is None

                future_state.register_status[current_state.instructions[idx].fi].qi = name

                future_state.instruction_stages[idx].wait = False
                return future_state
            
    if not fu_exists:
        raise RuntimeError(f"Functional unit {MAPPING[current_state.instructions[idx].op]} for operation {current_state.instructions[idx].op} does not exist.")

    future_state.instruction_stages[idx].wait = True
    return future_state

def read(
    current_state: SystemState,
    future_state: SystemState,
    idx: int # instruction index
):
    future_state.instruction_stages[idx].stage = Stage.READ
    fu_name = current_state.register_status[current_state.instructions[idx].fi].qi
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
    idx
):
    future_state.instruction_stages[idx].stage = Stage.EXECUTION
    fu_name = current_state.register_status[current_state.instructions[idx].fi].qi

    if current_state.instruction_status[idx].read is None:
        future_state.instruction_stages[idx].wait = True
        return future_state
    elif current_state.functional_units[fu_name].latency-1 > current_state.clock_cycle-current_state.instruction_status[idx].read:
        future_state.instruction_stages[idx].wait = True
        return future_state
    
    future_state.instruction_stages[idx].wait = False
    return future_state

def write(current_state, future_state, idx):
    future_state.instruction_stages[idx].stage = Stage.WRITE
    fu_name = current_state.register_status[current_state.instructions[idx].fi].qi
    for name, status in current_state.functional_unit_status.items():
        if name != fu_name and status.busy:
            if (status.fj == current_state.functional_unit_status[fu_name].fi and status.rj):
                future_state.instruction_stages[idx].wait = True
                return future_state
            if (status.fk == current_state.functional_unit_status[fu_name].fi and status.rk):
                future_state.instruction_stages[idx].wait = True
                return future_state

    for name, status in current_state.functional_unit_status.items():

        if status.qj == fu_name:
            future_state.functional_unit_status[name].qj = None
            future_state.functional_unit_status[name].rj = True

        if status.qk == fu_name:
            future_state.functional_unit_status[name].qk = None
            future_state.functional_unit_status[name].rk = True

    if current_state.register_status[current_state.functional_unit_status[fu_name].fi].qi == fu_name:
        future_state.register_status[current_state.functional_unit_status[fu_name].fi].qi = None

    future_state.functional_unit_status[fu_name] = FunctionalUnitStatus()
    future_state.instruction_stages[idx].wait = False

    return future_state
