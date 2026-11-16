import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solution_final import shortestPathAllKeys, read_maze

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_leetcode_examples_with_goal():
    # G에 처음 닿는 순간 종료. 열쇠는 자물쇠를 열 때만 필요
    assert shortestPathAllKeys(["@.a.G", "###.#", "b.A.B"]) == 4
    assert shortestPathAllKeys(["@..aA", "..B#.", "...Gb"]) == 5
    assert shortestPathAllKeys(["@Aa.G"]) == -1                     # 열쇠 a가 자물쇠 A 뒤에 있음

def test_goal_rules():
    assert shortestPathAllKeys(["@G.a"]) == 1                       # 열쇠를 안 모아도 G에 닿으면 끝
    assert shortestPathAllKeys(["@#G"]) == -1                       # G가 막혀 있음
    assert shortestPathAllKeys(["@.G"]) == 2
    assert shortestPathAllKeys(["@aAG"]) == 3                       # 열쇠로 자물쇠를 열고 G 도착
    assert shortestPathAllKeys(["@A.G"]) == -1                      # 열쇠 없이 자물쇠 통과 불가

def test_read_maze_validation(tmp_path=None):
    import tempfile
    d = tmp_path or tempfile.mkdtemp()
    for rows in (["@.a.."], ["@.GG"], ["@.x.G"], ["@..", "G."]):
        p = os.path.join(str(d), "bad.txt")
        with open(p, "w", encoding="utf-8") as fp:
            fp.write("\n".join(rows))
        try:
            read_maze(p)
        except ValueError:
            continue
        raise AssertionError(f"should reject {rows}")

def test_sample_building():
    grid = read_maze(os.path.join(ROOT, "grids", "sample_building.txt"))
    assert len(grid) == 9 and len(grid[0]) == 41
    assert shortestPathAllKeys(grid) == 47

# grids/test_case1~6: 기대하는 최단 이동 횟수 (test_case6은 G에 갈 수 없는 경우)
TEST_CASES = {
    "test_case1": 63,    # 3층
    "test_case2": 73,    # 3층
    "test_case3": 130,   # 3층
    "test_case4": 46,    # 2층 (3층 미만)
    "test_case5": 84,    # 4층 (3층 초과)
    "test_case6": -1,    # 3층, 열쇠 a는 자물쇠 B 뒤, 열쇠 b는 자물쇠 A 뒤, G도 자물쇠 A 뒤라 도달 불가
}

def test_grid_cases():
    for name, expected in TEST_CASES.items():
        grid = read_maze(os.path.join(ROOT, "grids", name))
        assert shortestPathAllKeys(grid) == expected, name

def test_case6_blocked_only_by_locks():
    # test_case6에서 열쇠 b 앞의 자물쇠 A 하나만 없애면 G에 갈 수 있어야 합니다 (막힌 이유가 자물쇠라는 확인)
    grid = read_maze(os.path.join(ROOT, "grids", "test_case6"))
    assert grid[3][25] == "A"
    grid[3][25] = "."
    assert shortestPathAllKeys(grid) == 53

if __name__ == "__main__":
    test_leetcode_examples_with_goal(); test_goal_rules(); test_read_maze_validation(); test_sample_building(); test_grid_cases(); test_case6_blocked_only_by_locks(); print("all tests passed")
