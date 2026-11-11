# Key-BFS on a Multi-floor Building (CSED331 PBL 1)

LeetCode 864 **Shortest Path to Get All Keys**에 **도착 지점 `G`**를 더한 변형(열쇠로 자물쇠를 열며 이동하고, `G`에 처음 닿는 순간 종료)을 3층 건물 grid에 적용하고, BFS 탐색 과정을 3D/2D로 시각화한 프로젝트입니다.
We apply a LeetCode 864 variant (pick up keys to open locks, stop at the goal `G`) to a 3-floor building grid and visualize the BFS over states `(row, col, mask)`.

**사이트 (Live):** https://lymph0.github.io/Algo_PBL1/

> 원래 LC 864 버전(열쇠를 다 모으는 순간 종료)은 `main` 브랜치에 있습니다.

## 구성 (Structure)

| 파일 | 설명 |
|---|---|
| `index.html` | 시각화 페이지 (3D 건물, 2D grid, 상태 공간 레이어, 코드 하이라이트, `solution3.py` 실행 결과 출력). 브라우저로 열면 바로 실행됩니다. |
| `solution3.py` | **최종 구현.** BFS (`shortestPathAllKeys`)와 입력 검사 (`load_grid`), 같은 폴더의 `input.txt` / `test_case_*.txt`를 읽어 최단 이동 횟수를 출력 |
| `solution.py` | 이전 버전 (모든 열쇠를 모은 뒤 G 도착) |
| `grids/sample_building.txt` | 예시 건물: 3개 층을 이어 붙인 grid 한 개 (9 × 41) |
| `tests/test_solution.py` | LeetCode 예제와 예시 건물 테스트 |

## 실행 (Run)

```bash
cp grids/sample_building.txt input.txt
python solution3.py                # input.txt: 최단 이동 횟수 = 47
python tests/test_solution.py      # 또는 pytest
```

시각화는 `index.html`을 브라우저로 여세요. (3D는 three.js r128을 CDN에서 불러오므로 인터넷 연결이 필요합니다.)

## Grid 기호 (Symbols)

`@` 시작 (start) · `#` 벽 (wall) · `.` 빈칸 (empty) · `a–f` 열쇠 (keys) · `A–F` 자물쇠 (locks) · `G` 도착 지점 (goal)

`@`와 `G`는 각각 정확히 하나여야 합니다. 자물쇠는 같은 글자의 열쇠를 이미 주웠을 때만 지나갈 수 있고, `G`에 처음 닿는 순간 종료합니다 (모든 열쇠를 모을 필요는 없습니다). `G`에 닿을 수 없으면 `-1`입니다.

## Grid 구성 방법 (How floors are joined)

입력은 **grid 한 개**입니다 (한 줄 = 한 행, 층 구분자 없음). 층별 도면을 같은 행끼리 `1F | 계단 열 | 2F | 계단 열 | 3F`로 이어 붙인 모양으로 씁니다.
예시 건물은 층 너비 13, 층 3개라 열 수가 `13 × 3 + 2 = 41`입니다. 계단 열은 계단인 행만 `.`, 나머지는 `#`라서, 다음 층으로 가려면 반드시 계단을 지나야 합니다.
계단은 아래층의 오른쪽 끝과 위층의 왼쪽 끝을 잇기 때문에, 3D에서는 2F를 좌우 반전해서 그려 계단이 같은 자리에 오도록 했습니다. 층 수는 시각화 페이지에서 3D로 나눠 그릴 때만 쓰이고, 알고리즘은 grid 한 개만 봅니다.

## 알고리즘 (Algorithm)

- **Why BFS**: 모든 이동 비용이 1이므로 BFS가 처음 `G` 칸을 꺼낸 순간이 최소 이동 횟수입니다.
- **State `(row, col, mask)`**: 같은 칸이라도 가진 열쇠가 다르면 다른 상태라 다시 방문해야 합니다.
- **Bitmask**: 열쇠 획득 `mask | (1 << i)`, 자물쇠 검사 `mask & (1 << i)`, 종료 조건 `grid[r][c] == 'G'`.
- **Complexity**: 시간·공간 모두 `O(m · n · 2^k)`. `k ≤ 6`이면 `2^k ≤ 64`인 상수이므로 `O(mn)`.
