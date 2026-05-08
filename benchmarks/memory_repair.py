import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.crystal.phase import reset_to_purifying
from core.immune import create_b_cell
from core.memory.reinforcer import reinforce


def main() -> None:
    cells = [create_b_cell("银行授信必须遵守风控政策。", "finance") for _ in range(100)]
    repaired = 0
    for cell in cells:
        cell.trust_score = 0.25
        reset_to_purifying(cell)
        for _ in range(20):
            reinforce(cell, 0.04)
        if cell.trust_score >= 0.8 and cell.crystal_state.phase == "reinforced":
            repaired += 1
    print({"samples": len(cells), "repaired": repaired, "repair_rate": repaired / len(cells)})


if __name__ == "__main__":
    main()
