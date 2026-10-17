"""Mengukur waktu algoritma buatan sendiri vs bawaan Python. Jalankan: python benchmark.py"""
import os
import random
import time

from services import algorithms


def waktu(fn, *a, ulang=3):
    terbaik = 1e9
    for _ in range(ulang):
        t = time.perf_counter()
        fn(*a)
        terbaik = min(terbaik, time.perf_counter() - t)
    return terbaik * 1000


def main():
    random.seed(1)
    baris = ["| n | insertion sort (ms) | merge sort (ms) | sorted() bawaan (ms) | linear search (ms) | binary search (ms) |",
             "|---|---|---|---|---|---|"]
    for n in (100, 1000, 5000):
        data = [random.randint(0, 10**6) for _ in range(n)]
        urut = sorted(data)
        target = urut[-1]
        ins = waktu(algorithms.insertion_sort, data, ulang=1 if n >= 5000 else 3)
        mrg = waktu(algorithms.merge_sort, data)
        bawaan = waktu(sorted, data)
        lin = waktu(algorithms.linear_search, urut, target, ulang=20)
        biner = waktu(algorithms.binary_search, urut, target, ulang=20)
        baris.append(f"| {n} | {ins:.3f} | {mrg:.3f} | {bawaan:.3f} | {lin:.4f} | {biner:.5f} |")
    teks = "\n".join(baris)
    print(teks)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "benchmark_algoritma.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("# Hasil Benchmark Algoritma\n\nDiukur dengan time.perf_counter (waktu terbaik dari beberapa kali jalan), data acak.\n\n" + teks + "\n")


if __name__ == "__main__":
    main()
