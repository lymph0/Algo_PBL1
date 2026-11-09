# Key-BFS on a Multi-floor Building (CSED331 PBL 1)

LeetCode 864 **Shortest Path to Get All Keys**를 3층 건물 grid에 적용하고, BFS 탐색 과정을 3D/2D로 시각화한 프로젝트입니다.
We apply LeetCode 864 to a 3-floor building grid and visualize the BFS over states `(row, col, keys)`.

## 구성 (Structure)

| 파일 | 설명 |
|---|---|
| `index.html` | 시각화 페이지 (3D 건물, 2D grid, 상태 공간 레이어, 코드 하이라이트). 브라우저로 열면 바로 실행됩니다. |
| `solution.py` | BFS 구현과 층별 grid 합치기 (`merge_floors`) |
| `grids/sample_building.txt` | 예시 건물 (층 사이 `---`, 오른쪽 끝 `S` = 다음 층 계단) |
| `tests/test_solution.py` | LeetCode 예제와 예시 건물 테스트 |

## 실행 (Run)

```bash
python solution.py                 # 예시 건물 → answer: 55
python tests/test_solution.py      # 또는 pytest
```

시각화는 `index.html`을 브라우저로 여세요. (3D는 three.js r128을 CDN에서 불러오므로 인터넷 연결이 필요합니다.)

## Grid 기호 (Symbols)

`@` 시작 (start) · `#` 벽 (wall) · `.` 빈칸 (empty) · `a–f` 열쇠 (keys) · `A–F` 자물쇠 (locks)

## Grid 구성 방법 (How floors are joined)

층별 grid를 같은 행끼리 `1F | 계단 열 | 2F | 계단 열 | 3F`로 이어 붙입니다. 계단 열은 계단 칸만 열고 나머지는 벽이라, 다음 층으로 가려면 반드시 계단을 지나야 합니다.
계단은 아래층의 오른쪽 끝과 위층의 왼쪽 끝을 잇기 때문에, 3D에서는 2F를 좌우 반전해서 그려 계단이 같은 자리에 오도록 했습니다.

## 알고리즘 (Algorithm)

- **Why BFS**: 모든 이동 비용이 1이므로 BFS가 처음 목표 상태에 도달한 순간이 최소 이동 횟수입니다.
- **State `(row, col, keys)`**: 같은 칸이라도 가진 열쇠가 다르면 다른 상태라 다시 방문해야 합니다.
- **Bitmask**: 열쇠 획득 `keys | (1 << i)`, 자물쇠 검사 `keys & (1 << i)`, 종료 조건 `keys == (1 << k) - 1`.
- **Complexity**: 시간·공간 모두 `O(m · n · 2^k)`. `k ≤ 6`이면 `2^k ≤ 64`인 상수이므로 `O(mn)`.
