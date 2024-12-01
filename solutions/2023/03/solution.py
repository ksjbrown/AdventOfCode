# Problem 3: https://adventofcode.com/2023/day/3

from __future__ import annotations
from collections import defaultdict
import itertools

from typing import Iterable

INPUT = "solutions/03/input.txt"

EMPTY = ""
DOT = "."
GEAR = "*"


class Glyph:
    def __init__(self, row: int, col: int, val: str) -> None:
        self.row = row
        self.col = col
        self.val = val

    def __repr__(self) -> str:
        return f"{self.row, self.col}:{self.val}"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Glyph) and (self.row == other.row and self.col == other.col and self.val == other.val)

    def __hash__(self) -> int:
        return (self.row, self.col, self.val).__hash__()

    @classmethod
    def parse(cls, line: str, row: int = 0) -> Iterable[Glyph]:
        buffer = EMPTY

        def buffer_yield(index: int) -> Glyph:
            nonlocal buffer
            val = buffer
            buffer = EMPTY
            return Glyph(row, index - len(val), val)

        for i, char in enumerate(line):
            if char != DOT:
                # only extend buffer if it will still be a number
                if buffer and not (char.isnumeric() and buffer.isnumeric()):
                    yield buffer_yield(i)
                buffer += char
                continue

            if char == DOT and buffer:
                yield buffer_yield(i)

    @property
    def top(self) -> int:
        return self.row

    @property
    def bottom(self) -> int:
        return self.row + 1

    @property
    def left(self) -> int:
        return self.col

    @property
    def right(self) -> int:
        return self.col + len(self.val)

    def intersects_horizontally(self, other) -> bool:
        return (self.left <= other.right) and (other.left <= self.right)

    def intersects_vertically(self, other) -> bool:
        return (self.top <= other.bottom) and (other.top <= self.bottom)

    def is_touching(self, other: Glyph) -> bool:
        return self.intersects_horizontally(other) and self.intersects_vertically(other)


def get_glyphs() -> Iterable[Glyph]:
    with open(INPUT, "r") as f:
        for i, line in enumerate(f):
            for glyph in Glyph.parse(line, i):
                yield glyph


def is_engine_code(glyph: Glyph) -> bool:
    return glyph.val.isnumeric()


def is_symbol(glyph: Glyph) -> bool:
    return not is_engine_code(glyph)


def is_gear(glyph: Glyph) -> bool:
    return glyph.val == GEAR


def adjacent_glyphs(glyphs: dict[int, list[Glyph]], glyph: Glyph) -> Iterable[Glyph]:
    for other in itertools.chain(glyphs[glyph.row - 1], glyphs[glyph.row], glyphs[glyph.row + 1]):
        if glyph.is_touching(other):
            yield other


def gear_ratio(glyphs: dict[int, list[Glyph]], glyph: Glyph) -> int:
    gear_pair: list[Glyph] = []

    for other in adjacent_glyphs(glyphs, glyph):
        if is_engine_code(other):
            gear_pair.append(other)

    if len(gear_pair) != 2:
        return 0

    return int(gear_pair[0].val) * int(gear_pair[1].val)


def part1() -> int:
    seen_glyphs: dict[int, list[Glyph]] = defaultdict(lambda: list())
    valid_engine_codes: set[Glyph] = set()

    for glyph in get_glyphs():
        # store all engine codes in a map
        # every time we encounter a symbol, check engine codes in this and previous row,
        # to see if this symbol is touching it
        # if it is, then the engine code is valid.
        seen_glyphs[glyph.row].append(glyph)

        if is_symbol(glyph):
            for prev_glyph in adjacent_glyphs(seen_glyphs, glyph):
                if is_engine_code(prev_glyph):
                    valid_engine_codes.add(prev_glyph)

        elif is_engine_code(glyph):
            for prev_glyph in adjacent_glyphs(seen_glyphs, glyph):
                if is_symbol(prev_glyph):
                    valid_engine_codes.add(glyph)
                    break  # only ever add the engine code once

    return sum(int(glyph.val) for glyph in valid_engine_codes)


def part2() -> int:
    seen_glyphs: dict[int, list[Glyph]] = defaultdict(lambda: list())
    ratios: dict[Glyph, int] = {}

    for glyph in get_glyphs():
        seen_glyphs[glyph.row].append(glyph)

        if is_gear(glyph):
            ratios[glyph] = gear_ratio(seen_glyphs, glyph)

        elif is_engine_code(glyph):
            for other in adjacent_glyphs(seen_glyphs, glyph):
                if is_gear(other):
                    ratios[glyph] = gear_ratio(seen_glyphs, other)

    return sum(ratios.values())


if __name__ == "__main__":
    print(part1())
    print(part2())
