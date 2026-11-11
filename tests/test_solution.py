import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solution3 import shortestPathAllKeys, load_grid

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

def test_load_grid_validation(tmp_path=None):
    import tempfile
    d = tmp_path or tempfile.mkdtemp()
    for rows in (["@.a.."], ["@.GG"], ["@.x.G"], ["@..", "G."]):
        p = os.path.join(str(d), "bad.txt")
        with open(p, "w", encoding="utf-8") as fp:
            fp.write("\n".join(rows))
        try:
            load_grid(p)
        except ValueError:
            continue
        raise AssertionError(f"should reject {rows}")

def test_sample_building():
    grid = load_grid(os.path.join(ROOT, "grids", "sample_building.txt"))
    assert len(grid) == 9 and len(grid[0]) == 41
    assert shortestPathAllKeys(grid) == 47

if __name__ == "__main__":
    test_leetcode_examples_with_goal(); test_goal_rules(); test_load_grid_validation(); test_sample_building(); print("all tests passed")
