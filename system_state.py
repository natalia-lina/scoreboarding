from basics import (
    FunctionalUnitStatus,
    RegisterStatus,
    InstructionStage
)


class SystemState:
    def __init__(
        self,
        fu_status: dict,
        reg_status: dict,
        instru_stages: list,
        clock_cycle: int
    ):
        self.fu_status = fu_status
        self.register_status = reg_status
        self.instru_stages = instru_stages
        self.clock_cycle = clock_cycle
    
    def show_fu_status(self):
        for name, fu in self.fu_status.items():
            print(name, fu.__dict__)

    def show_reg_status(self):
        for name, reg in self.register_status.items():
            print(name, reg.__dict__)
    
    def show_instru_stages(self):
        for idx, stage in enumerate(self.instru_stages):
            print(f"I{idx+1}", stage.__dict__)