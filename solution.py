"""LeetCode 864. Shortest Path to Get All Keys
BFS over states (row, col, keys) on a multi-floor building grid.
상태 (row, col, keys) 위에서 BFS를 돌려 모든 열쇠를 모으는 최소 이동 횟수를 구합니다.
"""
from collections import deque
from typing import List

DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def load_grid(path: str) -> List[str]:
    """이미 이어 붙인 grid 한 개를 읽습니다 (한 줄 = 한 행). Read one merged grid, one row per line."""
    with open(path, encoding="utf-8") as fp:
        rows = [line.strip() for line in fp if line.strip()]
    assert rows and all(len(r) == len(rows[0]) for r in rows), "every row must have the same length"
    return rows


def shortest_path_all_keys(grid: List[str]) -> int:
    m, n = len(grid), len(grid[0])
    k = 0
    for r in range(m):
        for c in range(n):
            ch = grid[r][c]
            if ch == "@":
                sr, sc = r, c
            elif ch.islower():
                k += 1
    full = (1 << k) - 1                      # all keys collected

    q = deque([(sr, sc, 0, 0)])              # (row, col, keys, moves)
    seen = {(sr, sc, 0)}
    while q:
        r, c, keys, moves = q.popleft()
        if keys == full:                     # keys == (1 << k) - 1
            return moves
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < m and 0 <= nc < n):
                continue                     # out of bounds
            ch = grid[nr][nc]
            if ch == "#":
                continue                     # wall
            nk = keys
            if ch.islower():
                nk |= 1 << (ord(ch) - ord("a"))          # pick up key: bitwise OR
            if ch.isupper() and not keys & (1 << (ord(ch) - ord("A"))):
                continue                     # lock without its key: bitwise AND
            if (nr, nc, nk) in seen:
                continue                     # state already visited
            seen.add((nr, nc, nk))
            q.append((nr, nc, nk, moves + 1))
    return -1


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "grids/sample_building.txt"
    grid = load_grid(path)
    print("\n".join(grid))
    print("answer:", shortest_path_all_keys(grid))
