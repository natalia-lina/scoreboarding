from re import split
from basics import (
    Instruction, Load, Store, FunctionalUnit,
    RegisterStatus, FunctionalUnitStatus, InstructionStatus, Pipeline, InstructionStage
)

def load_instructions(file_path: str) -> list[Instruction]:
    with open(file_path, "r") as f:
        instructions_input = f.read()

    lines = instructions_input.splitlines()

    instructions = []

    for line in lines:
        components = split(r"\s+", line.replace(",", ""))
        op = components[0]

        if op == "fld":
            instructions.append(Load(*components[1:]))
        
        elif op == "fsd":
            instructions.append(Store(*reversed(components[1:])))
        
        else:
            instructions.append(Instruction(*components))

    return instructions


def load_configurations(file_path: str) -> dict:
    with open(file_path, "r") as f:
        configurations_input = f.read()

    lines = configurations_input.splitlines()

    functional_units = {}
    for line in lines:
        components = split(r"\s+", line)
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
    instruction_stage = []

    for instru in instructions:
        if instru.fi is not None:
            register_status[instru.fi] = RegisterStatus()
        if instru.fj is not None:
            register_status[instru.fj] = RegisterStatus()
        if instru.fk is not None:
            register_status[instru.fk] = RegisterStatus()
        
        instruction_status.append(InstructionStatus())
        instruction_stage.append(InstructionStage())

    return register_status, instruction_status, instruction_stage

def instantitate_functional_unit_status(functional_units: dict) -> dict:
    function_unit_status = {}
    for name in functional_units.keys():
        function_unit_status[name] = FunctionalUnitStatus()
    return function_unit_status
