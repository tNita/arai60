from __future__ import annotations

import statistics
import timeit


def bench(fn, repeat: int = 9, number: int = 5) -> float:
    runs = timeit.Timer(fn).repeat(repeat=repeat, number=number)
    return statistics.median(runs) / number * 1000  # ms


def build_other(other_size: int, overlap: int) -> list[int]:
    return list(range(overlap)) + list(range(10_000, 10_000 + (other_size - overlap)))


def run_case(so_size: int, other: list[int], overlap: int) -> None:
    so = set(range(so_size))

    t_list = bench(lambda: so.intersection(other))
    t_convert = bench(lambda: so.intersection(set(other)))

    ratio = t_convert / t_list if t_list else float("inf")
    winner = "list" if t_list < t_convert else "convert"

    print(f"so={so_size:,}, other={len(other):,}, overlap={overlap:,}")
    print(f"intersection(list)      : {t_list:.3f} ms")
    print(f"intersection(set(list)) : {t_convert:.3f} ms")
    print(f"convert/list            : {ratio:.3f}x, winner={winner}")


def main() -> None:
    # so << other
    other_size = 1_000_000
    overlap = 1
    other = build_other(other_size, overlap)
    t_convert_only = bench(lambda: set(other))
    print(f"set(other) (1回だけ)    : {t_convert_only:.3f} ms\n")

    for so_size in [1, 4, 16, 64]:
        run_case(so_size=so_size, other=other, overlap=overlap)
        print()


if __name__ == "__main__":
    main()
