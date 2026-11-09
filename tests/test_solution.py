import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solution import shortest_path_all_keys, merge_floors, load_floors

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_leetcode_examples():
    assert shortest_path_all_keys(["@.a..", "###.#", "b.A.B"]) == 8
    assert shortest_path_all_keys(["@..aA", "..B#.", "....b"]) == 6
    assert shortest_path_all_keys(["@Aa"]) == -1

def test_sample_building():
    grid = merge_floors(load_floors(os.path.join(ROOT, "grids", "sample_building.txt")))
    assert len(grid) == 9 and len(grid[0]) == 41
    assert shortest_path_all_keys(grid) == 55

if __name__ == "__main__":
    test_leetcode_examples(); test_sample_building(); print("all tests passed")
