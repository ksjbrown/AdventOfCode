# Problem 1: https://adventofcode.com/2023/day/1

from typing import Callable, Iterable


INPUT = "solutions/01/input.txt"

WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def calculate(nums: Iterable[Iterable[int]]) -> int:
    sum_nums = 0
    for row in map(list, nums):
        assert len(row) > 0
        first = row[0]
        last = row[-1]
        sum_nums += first * 10 + last
    return sum_nums


def get_rows(path: str, row_get: Callable[[str], Iterable[int]]) -> Iterable[Iterable[int]]:
    """row_get should be a Callable that accepts a string,
    and returns the integers in the order they appear in the string.

    In Part 1, the integers are literal integer chars.
    In Part 2, the integers may also be words."""
    with open(path, "r") as f:
        for line in f:
            yield row_get(line)


def part1() -> int:
    def row_get(line: str) -> Iterable[int]:
        for char in line:
            if char.isnumeric():
                yield int(char)

    return calculate(get_rows(INPUT, row_get))


def part2() -> int:
    """Same as part1(), but do a replace of all words with digits in the line"""

    def row_get(line: str) -> Iterable[int]:
        for i in range(len(line)):
            # if char is numeric, we can immediately assume it is a number
            if line[i].isnumeric():
                yield int(line[i])
                continue
            # otherwise, we scan forward from current index and try to find a matching word
            for j in range(i + 1, len(line)):
                chunk = line[i:j]
                potential_matches = [word for word in WORDS if word.startswith(chunk)]

                # if no possible matches, abandon this chunk scan
                if len(potential_matches) == 0:
                    break

                # if we have an exact match, return the integer value and abandon scan
                if len(potential_matches) == 1 and potential_matches[0] == chunk:
                    digit = WORDS.get(chunk, None)
                    assert digit is not None
                    yield digit
                    break

    return calculate(get_rows(INPUT, row_get))


if __name__ == "__main__":
    print(part1())
    print(part2())
