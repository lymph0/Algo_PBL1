# Key-BFS on a Multi-floor Building (CSED331 PBL 1)

LeetCode 864 **Shortest Path to Get All Keys**에 **도착 지점 `G`**를 더한 변형(열쇠로 자물쇠를 열며 이동하고, `G`에 처음 닿는 순간 종료)을 여러 층 건물 grid에 적용하고, BFS 탐색 과정을 3D/2D로 시각화한 프로젝트입니다.
We apply a LeetCode 864 variant (pick up keys to open locks, stop at the goal `G`) to a multi-floor building grid and visualize the BFS over states `(row, col, mask)`.

**사이트 (Live):** https://lymph0.github.io/Algo_PBL1/

## 구성 (Structure)

| 파일 | 설명 |
|---|---|
| `index.html` | 시각화 페이지 (`건물` 선택에서 test_case1~6 / 예시 건물을 고를 수 있음, 3D 건물, 2D grid, 상태 공간 레이어, 코드 하이라이트, `solution_final.py` 실행 결과 출력). 브라우저로 열면 바로 실행됩니다. |
| `solution_final.py` | **최종 구현.** BFS (`shortestPathAllKeys`, `G`에 닿으면 종료)와 입력 검사 (`read_maze`). 파일 이름을 입력받아 미로와 `Shortest distance`를 출력 |
| `solution3.py` | 같은 규칙의 일괄 실행 버전 (같은 폴더의 `input.txt` / `test_case_*.txt`를 읽어 최단 이동 횟수 출력) |
| `solution2.py` | solution_final.py와 같은 내용의 이전 사본 |
| `solution.py` | 이전 버전 (모든 열쇠를 모은 뒤 G 도착) |
| `grids/sample_building.txt` | 예시 건물: 3개 층을 이어 붙인 grid 한 개 (9 × 41) |
| `grids/test_case1` ~ `test_case3` | 3층 건물 grid (9 × 41). 최단 이동 횟수 63 / 73 / 130 |
| `grids/test_case4` | 2층 건물 (3층 미만, 9 × 27). 최단 이동 횟수 46 |
| `grids/test_case5` | 4층 건물 (3층 초과, 7 × 39). 최단 이동 횟수 84 |
| `grids/test_case6` | 도달 불가능한 3층 건물 (7 × 29). 열쇠 a는 자물쇠 B 뒤, 열쇠 b와 G는 자물쇠 A 뒤에 있어서 `-1` |
| `tests/test_solution.py` | LeetCode 예제, 예시 건물, test_case1~6 테스트 |

## 실행 (Run)

```bash
python solution_final.py           # Maze file name: grids/sample_building.txt  →  Shortest distance: 47
python tests/test_solution.py      # 또는 pytest
```

시각화는 `index.html`을 브라우저로 여세요. (3D는 three.js r128을 CDN에서 불러오므로 인터넷 연결이 필요합니다.)

## Grid 기호 (Symbols)

`@` 시작 (start) · `#` 벽 (wall) · `.` 빈칸 (empty) · `a–f` 열쇠 (keys) · `A–F` 자물쇠 (locks) · `G` 도착 지점 (goal)

`@`와 `G`는 각각 정확히 하나여야 합니다. 자물쇠는 같은 글자의 열쇠를 이미 주웠을 때만 지나갈 수 있고, `G`에 처음 닿는 순간 종료합니다 (모든 열쇠를 모을 필요는 없습니다). `G`에 닿을 수 없으면 `-1`입니다.

## Grid 구성 방법 (How floors are joined)

입력은 **grid 한 개**입니다 (한 줄 = 한 행, 층 구분자 없음). 층별 도면을 같은 행끼리 `1F | 계단 열 | 2F | 계단 열 | 3F | …`로 이어 붙인 모양으로 씁니다. 층 수에는 제한이 없습니다.
예시 건물은 층 너비 13, 층 3개라 열 수가 `13 × 3 + 2 = 41`입니다. 계단 열은 계단인 행만 `.`, 나머지는 `#`라서, 다음 층으로 가려면 반드시 계단을 지나야 합니다.
계단은 아래층의 오른쪽 끝과 위층의 왼쪽 끝을 잇기 때문에, 3D에서는 2F를 좌우 반전해서 그려 계단이 같은 자리에 오도록 했습니다. 층 수는 따로 입력하지 않고 시각화 페이지가 자동으로 찾습니다. **빈칸 `.`이 정확히 한 칸이고 나머지가 모두 벽 `#`인 열**을 계단 열 후보로 보고, 층 너비가 모두 같다고 가정해 층 사이 자리(`W`, `2W+1`, …)의 열이 전부 계단 열 후보가 되는 층 수 중 가장 큰 값을 고릅니다. (방 안의 문 하나짜리 벽도 같은 모양이라, 층 사이 자리에 있는 열만 계단으로 봅니다.) 맞는 층 수가 없으면 1개 층으로 그립니다.
층 수는 시각화 페이지에서 3D로 나눠 그릴 때만 쓰이고, 알고리즘은 grid 한 개만 봅니다.

## 알고리즘 (Algorithm)

- **Why BFS**: 모든 이동 비용이 1이므로 BFS가 처음 `G` 칸을 꺼낸 순간이 최소 이동 횟수입니다.
- **State `(row, col, mask)`**: 같은 칸이라도 가진 열쇠가 다르면 다른 상태라 다시 방문해야 합니다.
- **Bitmask**: 열쇠 획득 `mask | (1 << i)`, 자물쇠 검사 `mask & (1 << i)`, 종료 조건 `grid[r][c] == 'G'`.
- **Complexity**: 시간·공간 모두 `O(m · n · 2^k)`. `k ≤ 6`이면 `2^k ≤ 64`인 상수이므로 `O(mn)`.
