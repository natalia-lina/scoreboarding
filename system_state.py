

from basics import (
    FunctionalUnitStatus,
    RegisterStatus,
    InstructionStage,
    InstructionStatus,
    Instruction,
    Stage
)


class SystemState:
    def __init__(
        self,
        instructions: list[Instruction],
        functional_units: dict
    ):
        self.__instructions = instructions
        self.__functional_units = functional_units
        
        self.register_status = {}
        self.instruction_status = []
        self.instruction_stages = []

        for instru in instructions:
            if instru.fi is not None:
                self.register_status[instru.fi] = RegisterStatus()
            if instru.fj is not None:
                self.register_status[instru.fj] = RegisterStatus()
            if instru.fk is not None:
                self.register_status[instru.fk] = RegisterStatus()
            
            self.instruction_status.append(InstructionStatus())
            self.instruction_stages.append(InstructionStage())

        self.functional_unit_status = {}
        for name in functional_units.keys():
            self.functional_unit_status[name] = FunctionalUnitStatus()

        self.clock_cycle = 0

    @property
    def instructions(self):
        return self.__instructions

    @property
    def functional_units(self):
        return self.__functional_units
    
    def copy(self):
        cp = SystemState(
            self.__instructions,
            self.__functional_units
        )

        for name, status in self.register_status.items():
            cp.register_status[name] = status.copy()

        for idx in range(len(self.__instructions)):
            cp.instruction_status[idx] = self.instruction_status[idx].copy()
            cp.instruction_stages[idx] = self.instruction_stages[idx].copy()

        for name, status in self.functional_unit_status.items():
            cp.functional_unit_status[name] = status.copy()

        cp.clock_cycle = self.clock_cycle

        return cp

    def update_instruction_status(self):
        for idx, stage in enumerate(self.instruction_stages):
            if stage.stage is None or stage.stage is Stage.DONE:
                continue
            if stage.stage is Stage.ISSUE:
                self.instruction_status[idx].issue = self.clock_cycle
            elif stage.stage is Stage.READ:
                self.instruction_status[idx].read = self.clock_cycle
            elif stage.stage is Stage.EXECUTION:
                self.instruction_status[idx].execution = self.clock_cycle
            elif stage.stage is Stage.WRITE:
                self.instruction_status[idx].write = self.clock_cycle

    def finished(self):
        if self.clock_cycle < 4:
            return False

        for status in self.functional_unit_status.values():
            if status.busy:
                return False

        for status in self.register_status.values():
            if status.qi is not None:
                return False

        for status in self.instruction_status:
            if status.write is None:
                return False
            if status.write <= self.clock_cycle:
                continue
            else:
                return False
        
        return True

    def show_fu_status(self):
        for name, fu in self.functional_unit_status.items():
            print(name, fu.__dict__)

    def show_register_status(self):
        for name, reg in self.register_status.items():
            print(name, reg.__dict__)
    
    def show_instru_stages(self):
        for idx, stage in enumerate(self.instruction_stages):
            print(f"I{idx+1}", stage.__dict__)

    def show_instru_status(self):
        for idx, status in enumerate(self.instruction_status):
            print(f"I{idx+1}", status.__dict__)
