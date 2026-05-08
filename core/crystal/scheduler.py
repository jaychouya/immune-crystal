from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler

from core.crystal.fourier import fold_noise
from core.crystal.oscillator import CrystalOscillator
from core.memory.store import MemoryStore


class CrystalScheduler:
    def __init__(self, store: MemoryStore, interval_seconds: int = 30) -> None:
        self.store = store
        self.interval_seconds = interval_seconds
        self.oscillator = CrystalOscillator()
        self.scheduler = BackgroundScheduler()

    def start(self) -> None:
        if self.scheduler.running:
            return
        self.scheduler.add_job(self.run_cycle, "interval", seconds=self.interval_seconds, id="crystal")
        self.scheduler.start()

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)

    def run_cycle(self) -> None:
        for cell in self.store.list():
            cell = self.oscillator.tick(cell)
            cell = fold_noise(cell)
            self.store.update(cell)
