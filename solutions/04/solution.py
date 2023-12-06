# Problem 4: https://adventofcode.com/2023/day/4

from __future__ import annotations
from collections import defaultdict

from typing import Iterable, Self

INPUT = "solutions/04/input.txt"

EMPTY = ""
COLON = ":"
PIPE = "|"

CARD = "Card"


class Card:
    def __init__(
        self, index: int, winning_numbers: list[int], numbers: list[int]
    ) -> None:
        self.index = index
        self.winning_numbers = winning_numbers
        self.numbers = numbers

    @classmethod
    def parse(cls, line: str) -> Self:
        index_chunk, all_numbers_chunk = line.split(COLON)
        index = int(index_chunk.replace(CARD, EMPTY).strip())

        winning_numbers_chunk, numbers_chunk = all_numbers_chunk.split(PIPE)
        winning_numbers = [
            int(number.strip()) for number in winning_numbers_chunk.split()
        ]
        numbers = [int(number.strip()) for number in numbers_chunk.split()]

        return cls(index, winning_numbers, numbers)

    @property
    def matches(self) -> int:
        return len(
            [number for number in self.numbers if number in self.winning_numbers]
        )


def get_cards() -> Iterable[Card]:
    with open(INPUT, "r") as f:
        for line in f:
            yield Card.parse(line)


def part1() -> int:
    def score(card: Card):
        return 0 if card.matches == 0 else 2 ** (card.matches - 1)

    return sum(score(card) for card in get_cards())


def part2() -> int:
    card_counts: dict[int, int] = defaultdict(lambda: 1)
    for card in get_cards():
        count = card_counts[card.index]
        for i in range(card.matches):
            card_counts[card.index + i + 1] += count
    return sum(card_counts.values())


if __name__ == "__main__":
    print(part1())
    print(part2())
