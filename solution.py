"""LeetCode 864. Shortest Path to Get All Keys
BFS over states (row, col, keys) on a multi-floor building grid.
상태 (row, col, keys) 위에서 BFS를 돌려 모든 열쇠를 모으는 최소 이동 횟수를 구합니다.
"""
from collections import deque
from typing import List

DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def merge_floors(floors: List[List[str]]) -> List[str]:
    """층별 grid를 같은 행끼리 이어 붙입니다 (1F | 계단 열 | 2F | 계단 열 | 3F).
    각 층의 맨 오른쪽 열에 'S'가 있으면 그 행의 계단 열을 열고, 나머지는 벽 '#'으로 막습니다.
    Join floors row by row; an 'S' in a floor's rightmost column opens a stair to the next floor.
    """
    h, w = len(floors[0]), len(floors[0][0])
    for f in floors:
        assert len(f) == h and all(len(row) == w for row in f), "all floors must have the same size"
    rows = []
    for r in range(h):
        s = ""
        for i, f in enumerate(floors):
            s += f[r].replace("S", ".")
            if i < len(floors) - 1:
                s += "." if f[r][w - 1] == "S" else "#"
        rows.append(s)
    return rows


def load_floors(path: str) -> List[List[str]]:
    """'---' 줄로 층을 구분한 텍스트 파일을 읽습니다. Floors are separated by a '---' line."""
    floors, cur = [], []
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            if set(line) == {"-"}:
                floors.append(cur)
                cur = []
            else:
                cur.append(line)
    if cur:
        floors.append(cur)
    return floors


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
    grid = merge_floors(load_floors(path))
    print("\n".join(grid))
    print("answer:", shortest_path_all_keys(grid))
