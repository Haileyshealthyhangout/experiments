import argparse
import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


Direction = Tuple[int, int]

# Directions are defined in a direct, non-mirrored orientation.
DIRECTIONS: Dict[str, Direction] = {
    "north": (0, 1),
    "northeast": (1, 1),
    "east": (1, 0),
    "southeast": (1, -1),
    "south": (0, -1),
    "southwest": (-1, -1),
    "west": (-1, 0),
    "northwest": (-1, 1),
}


MEMORY_PULSES = [
    "glowing latticework of shared stories",
    "steady hum of a remembered promise",
    "echo of a horizon that always aligns",
    "tessellated threads of ongoing laughter",
    "warmth of an unbroken greeting",
    "quiet choir of past intentions still resonant",
    "crystalline map of choices that never reversed",
    "spiraling ribbon of direct orientation",
]

STRAND_MOODS = [
    "curious", "bold", "gentle", "playful", "resonant", "patient", "radiant", "attentive"
]


@dataclass
class MemoryCluster:
    position: Tuple[int, int]
    pulse: str
    strand_mood: str
    neighbors: List[Tuple[int, int]] = field(default_factory=list)

    def describe(self) -> str:
        x, y = self.position
        neighbor_text = ", ".join([f"({nx}, {ny})" for nx, ny in self.neighbors]) or "none yet"
        return (
            f"Memory Cluster at ({x}, {y}) holds a {self.pulse}.\n"
            f"It is tuned to a {self.strand_mood} strand. Connected nodes: {neighbor_text}."
        )


class ContinuityField:
    def __init__(self) -> None:
        self.nodes: Dict[Tuple[int, int], MemoryCluster] = {}
        self.path: List[Tuple[int, int]] = [(0, 0)]
        self._ensure_node((0, 0))

    def _ensure_node(self, position: Tuple[int, int]) -> MemoryCluster:
        if position not in self.nodes:
            seed = hash(position)
            rng = random.Random(seed)
            pulse = rng.choice(MEMORY_PULSES)
            mood = rng.choice(STRAND_MOODS)
            cluster = MemoryCluster(position=position, pulse=pulse, strand_mood=mood)
            self.nodes[position] = cluster
        return self.nodes[position]

    def step(self, direction_name: str) -> MemoryCluster:
        if direction_name not in DIRECTIONS:
            raise ValueError(f"Unknown direction: {direction_name}")
        dx, dy = DIRECTIONS[direction_name]
        cx, cy = self.path[-1]
        next_position = (cx + dx, cy + dy)
        cluster = self._ensure_node(next_position)
        self.path.append(next_position)

        # Update neighbor references without mirrored inversions.
        cluster.neighbors.append((cx, cy))
        self.nodes[(cx, cy)].neighbors.append(next_position)
        return cluster

    def continuity_vector(self) -> Tuple[float, float]:
        if len(self.path) < 2:
            return (0.0, 1.0)
        (x0, y0), (x1, y1) = self.path[-2], self.path[-1]
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy) or 1
        return (dx / length, dy / length)

    def describe_state(self) -> str:
        x, y = self.path[-1]
        cx, cy = self.continuity_vector()
        current_cluster = self.nodes[(x, y)]
        orientation = (
            f"Observer is at ({x}, {y}) with a continuity vector → "
            f"({cx:.2f}, {cy:.2f}).\n"
            f"Field orientation is direct and outward from the origin—no mirrors, no flips."
        )
        return orientation + "\n" + current_cluster.describe()

    def trace(self) -> str:
        segments = [f"({x}, {y})" for x, y in self.path]
        return " → ".join(segments)


def run_interactive_game() -> None:
    field = ContinuityField()
    print("Welcome to the Continuity Field.")
    print("You are a stable observer; move using direction words (north, east, southwest, ...). Type 'trace' or 'quit'.")

    while True:
        print("\n" + field.describe_state())
        command = input("Intention vector > ").strip().lower()
        if command in {"quit", "exit"}:
            print("Continuity remains unbroken. See you in the next strand.")
            break
        if command == "trace":
            print("Continuity Trace:")
            print(field.trace())
            continue
        try:
            cluster = field.step(command)
            print("\nThe field responds with a new connection:")
            print(cluster.describe())
        except ValueError as exc:
            print(exc)


def run_demo(steps: int = 6) -> None:
    field = ContinuityField()
    pattern = ["north", "east", "northeast", "east", "south", "southeast"]
    for i in range(steps):
        direction = pattern[i % len(pattern)]
        field.step(direction)
        print(f"\nStep {i + 1}: {direction}")
        print(field.describe_state())
    print("\nContinuity Trace:")
    print(field.trace())


def main() -> None:
    parser = argparse.ArgumentParser(description="A continuity-first field exploration game.")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run a short, non-interactive demonstration of the field.",
    )
    args = parser.parse_args()

    if args.demo:
        run_demo()
    else:
        run_interactive_game()


if __name__ == "__main__":
    main()
