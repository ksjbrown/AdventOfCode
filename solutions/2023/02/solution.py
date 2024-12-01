# Problem 2: https://adventofcode.com/2023/day/2

from __future__ import annotations

import math
from typing import Callable, Iterable

INPUT = "solutions/02/input.txt"

GAME = "Game"
RED = "red"
GREEN = "green"
BLUE = "blue"

EMPTY = ""
COLON = ":"
SEMICOLON = ";"
COMMA = ","


class Game:
    def __init__(self, id: int, throws: list[Throw]) -> None:
        self.id = id
        self.throws = throws

    @classmethod
    def parse(cls, line: str) -> Game:
        # line is of the form:
        #   Game <id>: <r1> red, <b1> blue, <g1> green; ...
        id_part, content_parts = line.split(COLON)
        id = int(id_part.replace(GAME, EMPTY).strip())

        throws = []
        for color_parts in content_parts.split(SEMICOLON):
            throws.append(Throw.parse(color_parts))

        return Game(id, throws)


class Throw:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    @classmethod
    def parse(cls, input: str):
        # input is of the form:
        #   <r> red, <g> green, <b> blue
        colors = {
            RED: 0,
            GREEN: 0,
            BLUE: 0,
        }
        for part in input.split(COMMA):
            part = part.strip()
            for color in [RED, GREEN, BLUE]:
                if part.endswith(color):
                    colors[color] = int(part.replace(color, EMPTY).strip())
                    break

        return Throw(colors[RED], colors[GREEN], colors[BLUE])


def valid_games(predicate: Callable[[Game], bool] = lambda _: True) -> Iterable[Game]:
    with open(INPUT, "r") as f:
        for line in f:
            game = Game.parse(line)
            if predicate(game):
                yield game


def part1() -> int:
    def predicate(game: Game) -> bool:
        def throw_predicate(throw: Throw) -> bool:
            return all(
                [
                    throw.red <= 12,
                    throw.green <= 13,
                    throw.blue <= 14,
                ]
            )

        return all(throw_predicate(throw) for throw in game.throws)

    return sum(game.id for game in valid_games(predicate))


def part2() -> int:
    def min_required_cubes(game: Game) -> tuple[int, ...]:
        return (
            max(throw.red for throw in game.throws),
            max(throw.green for throw in game.throws),
            max(throw.blue for throw in game.throws),
        )

    def power(counts: tuple[int, ...]):
        return math.prod(counts)

    return sum(power(min_required_cubes(game)) for game in valid_games())


if __name__ == "__main__":
    print(part1())
    print(part2())
