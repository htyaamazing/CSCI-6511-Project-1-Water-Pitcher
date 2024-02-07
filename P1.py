import heapq
from functools import reduce
import math
class State:
    def __init__(self, pitchers, infinite, cost):
        self.pitchers = pitchers
        self.infinite = infinite
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost


def heuristic(target, infinite):
    return abs(target - infinite)
def gcd(a, b):
    """计算两个数的最大公约数。"""
    while b:
        a, b = b, a % b
    return a

def find_gcd(list):
    """计算一组数的最大公约数。"""
    x = reduce(gcd, list)
    return x

def generate_successors(state, capacities):
    successors = []
    for i, water in enumerate(state.pitchers):
        # 尝试清空或填满每个有限容量水壶，并更新状态
        new_pitchers_fill = state.pitchers.copy()
        new_pitchers_fill[i] = capacities[i]
        successors.append(State(new_pitchers_fill, state.infinite, state.cost + 1))

        if water > 0:
            new_pitchers_empty = state.pitchers.copy()
            new_pitchers_empty[i] = 0
            successors.append(State(new_pitchers_empty, state.infinite + water, state.cost + 1))

    return successors


def can_target_be_reached(capacities, target):
    # 检查目标量是否可达的简单逻辑
    if target > sum(capacities):
        return False
    return True


def astar(capacities, target):
    # 检查目标是否可达：目标量必须是所有水壶容量的最大公约数的倍数
    if target % find_gcd(capacities) != 0:
        return -1

    start_state = State([0] * len(capacities), 0, 0)
    frontier = [(heuristic(target, start_state.infinite), start_state)]
    explored = set()

    while frontier:
        _, current_state = heapq.heappop(frontier)
        if current_state.infinite >= target:  # 目标达成条件调整为 >=
            return current_state.cost

        current_key = tuple(current_state.pitchers) + (current_state.infinite,)
        if current_key in explored:
            continue
        explored.add(current_key)

        for succ in generate_successors(current_state, capacities):
            succ_key = tuple(succ.pitchers) + (succ.infinite,)
            if succ_key not in explored:
                heapq.heappush(frontier, (succ.cost + heuristic(target, succ.infinite), succ))

    return -1



def solve_water_pitcher_problem(filepath):
    with open(filepath, 'r') as file:
        capacities = list(map(int, file.readline().strip().split(',')))
        target = int(file.readline().strip())
    steps = astar(capacities, target)
    if steps == -1:
        print("no path")
    else:
        print(f"steps: {steps}")


# 示例使用
filepath = "cat input4.txt"
solve_water_pitcher_problem(filepath)