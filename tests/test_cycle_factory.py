
# test in tests NOT tests/backend

from backend.cycle_factory import CycleFactory
from backend.memory_adapter import MemoryAdapter, CycleRecord


class FakeMemory(MemoryAdapter):
    def __init__(self, records):
        super().__init__()
        self._records = records

    def load_cycle_records(self):
        self.last_call = ("load_cycle_records", (), {})
        return self._records


def test_cycle_factory_calls_layer2_and_returns_names():
    records = [
        CycleRecord(cycle_name="Cycle A", cycle_duration=10.0),
        CycleRecord(cycle_name="Cycle B", cycle_duration=20.0),
    ]
    mem = FakeMemory(records)
    factory = CycleFactory(memory=mem)

    names = factory.get_available_cycles()

    assert mem.last_call is not None
    assert mem.last_call[0] == "load_cycle_records"
    assert names == ["Cycle A", "Cycle B"]