from re import split
from basics import (
    Instruction, Load, Store, FunctionalUnit,
    RegisterStatus, FunctionalUnitStatus, InstructionStatus, Pipeline, InstructionStage
)

def load_inputs(
    instruction_file_path: str,
    configuration_file_path: str
):

    with open(instruction_file_path, "r") as f:
        instructions_input = f.read().splitlines()

    with open(configuration_file_path, "r") as f:
        configurations_input = f.read().splitlines()

    return (
        parse_instructions(instructions_input),
        parse_configurations(configurations_input)
    )

def parse_instructions(instructions_input: list[str]) -> list[Instruction]:

    instructions = []

    for line in instructions_input:
        components = split(r"\s+", line.replace(",", ""))
        op = components[0]

        if op == "fld":
            instructions.append(Instruction(*components, None))
        
        elif op == "fsd":
            instructions.append(Instruction(op, components[-1], components[-2], None))
        
        else:
            instructions.append(Instruction(*components))

    return instructions


def parse_configurations(configurations_input: list[str]) -> dict:

    functional_units = {}
    for line in configurations_input:
        components = split(r"\s+", line)
        kind = components[0]
        num = int(components[1])
        lat = int(components[2])

        fu = FunctionalUnit(kind, lat)

        for idx in range(num):
            functional_units[f"{kind}{idx+1}"] = fu
    
    return functional_units
