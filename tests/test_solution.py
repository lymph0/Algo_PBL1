import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solution import shortestPathAllKeys, merge_floors, load_floors

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_leetcode_examples_with_goal():
    # LeetCode 864 예제에 G를 추가: 열쇠를 다 모은 뒤 G까지 가야 함
    assert shortestPathAllKeys(["@.a.G", "###.#", "b.A.B"]) == 14
    assert shortestPathAllKeys(["@..aA", "..B#.", "...Gb"]) == 7
    assert shortestPathAllKeys(["@Aa.G"]) == -1

def test_goal_rules():
    assert shortestPathAllKeys(["@.a..", "###.#", "b.A.B"]) == -1   # G가 없으면 도착 불가
    assert shortestPathAllKeys(["@G.a"]) == 5                       # 열쇠 전에 G를 지나쳐도 계속 탐색
    assert shortestPathAllKeys(["@#G"]) == -1                       # G가 막혀 있음
    assert shortestPathAllKeys(["@.G"]) == 2                        # 열쇠가 없으면 G까지 최단 거리

def test_sample_building():
    grid = merge_floors(load_floors(os.path.join(ROOT, "grids", "sample_building.txt")))
    assert len(grid) == 9 and len(grid[0]) == 41
    assert shortestPathAllKeys(grid) == 65

if __name__ == "__main__":
    test_leetcode_examples_with_goal(); test_goal_rules(); test_sample_building(); print("all tests passed")
