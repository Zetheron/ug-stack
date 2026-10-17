"""Algoritma pencarian dan pengurutan buatan sendiri (tanpa sorted()/list.sort()).

Kompleksitas:  linear_search O(n) | binary_search O(log n) pada data terurut |
               insertion_sort O(n^2) terburuk, O(n) hampir terurut | merge_sort O(n log n), stabil.
"""


def _same(x):
    return x


def linear_search(items: list, target, key=_same) -> int:
    """Mengembalikan indeks pertama yang cocok, atau -1."""
    for i in range(len(items)):
        if key(items[i]) == target:
            return i
    return -1


def binary_search(sorted_items: list, target, key=_same) -> int:
    """Pencarian biner. Prasyarat: sorted_items sudah terurut naik menurut key."""
    low, high = 0, len(sorted_items) - 1
    while low <= high:                       # perulangan while: persempit rentang
        mid = (low + high) // 2
        value = key(sorted_items[mid])
        if value == target:
            return mid
        if value < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def is_sorted(items: list, key=_same) -> bool:
    return all(key(items[i]) <= key(items[i + 1]) for i in range(len(items) - 1))


def insertion_sort(items: list, key=_same, descending: bool = False) -> list:
    """Mengembalikan salinan terurut (stabil)."""
    result = list(items)
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0 and _after(key(result[j]), key(current), descending):
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result


def _after(a, b, descending: bool) -> bool:
    """True bila a harus berada SETELAH b (a perlu digeser)."""
    return a < b if descending else a > b


def merge_sort(items: list, key=_same, descending: bool = False) -> list:
    """Mengembalikan salinan terurut (stabil), waktu O(n log n)."""
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    left = merge_sort(items[:mid], key, descending)
    right = merge_sort(items[mid:], key, descending)
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        take_left = key(left[i]) >= key(right[j]) if descending else key(left[i]) <= key(right[j])
        if take_left:                        # ambil kiri saat sama -> stabil
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
