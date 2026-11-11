from collections import deque
from pathlib import Path


def load_grid(file_path):
    """Read a maze from a UTF-8 text file (one row per line)."""
    text = Path(file_path).read_text(encoding="utf-8-sig")
    grid = [line.strip() for line in text.splitlines() if line.strip()]

    if not grid:
        raise ValueError("미로가 비어 있습니다.")
    if any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("모든 행의 길이가 같아야 합니다.")
    if sum(row.count('@') for row in grid) != 1:
        raise ValueError("출발점 @는 정확히 하나여야 합니다.")
    if sum(row.count('G') for row in grid) != 1:
        raise ValueError("도착점 G는 정확히 하나여야 합니다.")

    allowed = set("#.@GabcdefABCDEF")
    if any(cell not in allowed for row in grid for cell in row):
        raise ValueError("미로에 알 수 없는 문자가 있습니다.")

    return grid


def shortestPathAllKeys(grid):
    m, n = len(grid), len(grid[0])
    start = None
    target = 0

    for r in range(m):
        for c in range(n):
            cell = grid[r][c]
            if cell == '@':
                start = (r, c)
            elif 'a' <= cell <= 'f':
                target |= 1 << (ord(cell) - ord('a'))

    queue = deque([(start[0], start[1], 0, 0)])
    visited = {(start[0], start[1], 0)}
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        r, c, mask, dist = queue.popleft()

        # 도착점 G에 도착하면 종료합니다. (자물쇠는 해당 열쇠가 있어야 통과)
        if grid[r][c] == 'G':
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < m and 0 <= nc < n):
                continue

            cell = grid[nr][nc]
            if cell == '#':
                continue

            if 'A' <= cell <= 'F':
                bit = 1 << (ord(cell) - ord('A'))
                if not (mask & bit):
                    continue

            new_mask = mask
            if 'a' <= cell <= 'f':
                new_mask |= 1 << (ord(cell) - ord('a'))

            state = (nr, nc, new_mask)
            if state in visited:
                continue

            visited.add(state)
            queue.append((nr, nc, new_mask, dist + 1))

    return -1


def main():
    folder = Path(__file__).resolve().parent

    # 같은 폴더의 input.txt(있는 경우) 및 test_case_*.txt를 자동으로 탐색합니다.
    paths = sorted(folder.glob('test_case_*.txt'))
    if (folder / 'input.txt').is_file():
        paths.insert(0, folder / 'input.txt')

    if not paths:
        print('입력 파일이 없습니다. input.txt 또는 test_case_*.txt를 같은 폴더에 넣어주세요.')
        return

    for path in paths:
        try:
            grid = load_grid(path)
            answer = shortestPathAllKeys(grid)
            print(f'{path.name}: 최단 이동 횟수 = {answer}')
        except (OSError, UnicodeError, ValueError) as exc:
            print(f'{path.name}: 입력 오류 - {exc}')


if __name__ == '__main__':
    main()
