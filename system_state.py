from basics import (
    FunctionalUnitStatus,
    RegisterStatus,
    InstructionStage,
    InstructionStatus,
    Pipeline
)


class SystemState:
    def __init__(
        self,
        fu_status: dict,
        reg_status: dict,
        instru_status: list,
        instru_stages: list,
        clock_cycle: int
    ):
        self.fu_status = fu_status
        self.register_status = reg_status
        self.instru_status = instru_status
        self.instru_stages = instru_stages
        self.clock_cycle = clock_cycle
    
    def update_instruction_status(self):
        for idx, stage in enumerate(self.instru_stages):
            if stage.stage is None or stage.stage is Pipeline.DONE:
                continue
            if stage.stage is Pipeline.ISSUE:
                self.instru_status[idx].issue = self.clock_cycle
            elif stage.stage is Pipeline.READ:
                self.instru_status[idx].read = self.clock_cycle
            elif stage.stage is Pipeline.EXECUTION:
                self.instru_status[idx].execution = self.clock_cycle
            elif stage.stage is Pipeline.WRITE:
                self.instru_status[idx].write = self.clock_cycle

    def show_fu_status(self):
        for name, fu in self.fu_status.items():
            print(name, fu.__dict__)

    def show_reg_status(self):
        for name, reg in self.register_status.items():
            print(name, reg.__dict__)
    
    def show_instru_stages(self):
        for idx, stage in enumerate(self.instru_stages):
            print(f"I{idx+1}", stage.__dict__)

    def show_instru_status(self):
        for idx, status in enumerate(self.instru_status):
            print(f"I{idx+1}", status.__dict__)