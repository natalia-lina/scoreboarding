from basics import (
    Instruction, Load, Store, FunctionalUnit,
    RegisterStatus, FunctionalUnitStatus, InstructionStatus, Pipeline
)

def load_instructions(instructions_input: str) -> list[Instruction]:
    lines = instructions_input.splitlines()

    instructions = []

    for line in lines:
        components = line.replace(",", "").split(" ")
        op = components[0]

        if op == "fld":
            instructions.append(Load(*components[1:]))
        
        elif op == "fsd":
            instructions.append(Store(*components[1:]))
        
        else:
            instructions.append(Instruction(*components))

    return instructions


def load_configurations(configurations_input: str) -> dict:
    lines = configurations_input.splitlines()

    functional_units = {}
    for line in lines:
        components = line.split(" ")
        kind = components[0]
        num = int(components[1])
        lat = int(components[2])

        fu = FunctionalUnit(kind, lat)

        for idx in range(num):
            functional_units[f"{kind}{idx+1}"] = fu
    
    return functional_units

def instantiate_registers_instructions_status(instructions: list) -> tuple:
    register_status = {}
    instruction_status = []

    for instru in instructions:
        if instru.fi is not None:
            register_status[instru.fi] = RegisterStatus()
        if instru.fj is not None:
            register_status[instru.fj] = RegisterStatus()
        if instru.fk is not None:
            register_status[instru.fk] = RegisterStatus()
        
        instruction_status.append(InstructionStatus())

    return register_status, instruction_status

def instantitate_functional_unit_status(functional_units: dict) -> dict:
    function_unit_status = {}
    for name in functional_units.keys():
        function_unit_status[name] = FunctionalUnitStatus()
    return function_unit_status
