
# test in tests NOT tests/backend

from backend.cycle import Cycle
from backend.memory_adapter import MemoryAdapter


class FakeMemory(MemoryAdapter):
    def load_cycle_instructions(self, location: str) -> str:
        self.last_call = ("load_cycle_instructions", (location,), {})
        return "INSTRUCTIONS"


def test_cycle_load_instructions_calls_layer2():
    mem = FakeMemory()
    c = Cycle(
        name="Cycle A",
        duration_sec=10.0,
        instructions_location="resources/cycles/cycle_a.txt"
    )

    text = c.load_instructions(mem)

    assert text == "INSTRUCTIONS"
    assert mem.last_call is not None
    assert mem.last_call[0] == "load_cycle_instructions"
    assert mem.last_call[1][0] == "resources/cycles/cycle_a.txt"