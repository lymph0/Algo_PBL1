"""LeetCode 864 variant: collect all keys, then reach the goal 'G'.
상태 (row, col, mask) 위에서 BFS를 돌려, 모든 열쇠를 모은 뒤 도착 지점 G에 닿는 최소 이동 횟수를 구합니다.
"""
from collections import deque
from typing import List


def load_grid(path: str) -> List[str]:
    """이미 이어 붙인 grid 한 개를 읽습니다 (한 줄 = 한 행). Read one merged grid, one row per line."""
    with open(path, encoding="utf-8") as fp:
        rows = [line.strip() for line in fp if line.strip()]
    assert rows and all(len(r) == len(rows[0]) for r in rows), "every row must have the same length"
    return rows


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
    grid = load_grid(path)
    print("\n".join(grid))
    print("answer:", shortestPathAllKeys(grid))
