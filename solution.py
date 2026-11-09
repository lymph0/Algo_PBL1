"""LeetCode 864 variant: collect all keys, then reach the goal 'G'.
상태 (row, col, mask) 위에서 BFS를 돌려, 모든 열쇠를 모은 뒤 도착 지점 G에 닿는 최소 이동 횟수를 구합니다.
"""
from collections import deque
from typing import List


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


def shortestPathAllKeys(grid):
    m, n = len(grid), len(grid[0])

    start = None
    total_keys = 0

    # 시작점과 열쇠 개수 확인
    for r in range(m):
        for c in range(n):
            if grid[r][c] == '@':
                start = (r, c)

            if 'a' <= grid[r][c] <= 'f':
                total_keys += 1

    # 모든 열쇠를 획득한 상태
    target = (1 << total_keys) - 1

    # BFS 초기화
    queue = deque([(start[0], start[1], 0, 0)])
    visited = set()
    visited.add((start[0], start[1], 0))

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        r, c, mask, dist = queue.popleft()

        # 모든 열쇠를 획득하고 목표 지점에 도착
        if mask == target and grid[r][c] == 'G':
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # 격자 범위 확인
            if not (0 <= nr < m and 0 <= nc < n):
                continue

            cell = grid[nr][nc]

            # 벽 확인
            if cell == '#':
                continue

            # 자물쇠 확인
            if 'A' <= cell <= 'F':
                bit = 1 << (ord(cell) - ord('A'))

                if not (mask & bit):
                    continue

            # 열쇠 획득
            new_mask = mask

            if 'a' <= cell <= 'f':
                bit = 1 << (ord(cell) - ord('a'))
                new_mask |= bit

            # 방문 여부 확인
            state = (nr, nc, new_mask)

            if state in visited:
                continue

            visited.add(state)
            queue.append((nr, nc, new_mask, dist + 1))

    return -1


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "grids/sample_building.txt"
    grid = merge_floors(load_floors(path))
    print("\n".join(grid))
    print("answer:", shortestPathAllKeys(grid))
