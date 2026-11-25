from collections import deque
from itertools import permutations

def solve_maze(grid):
    rows = len(grid)
    cols = len(grid[0])
    start = (0, 0)
    goal  = (rows - 1, cols - 1)

    cheeses = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                cheeses.append((r, c))

    n_cheese = len(cheeses)

    def bfs_from(src):
        dist   = [[-1] * cols for _ in range(rows)]
        parent = [[None]      * cols for _ in range(rows)]
        sr, sc = src
        dist[sr][sc] = 0
        q = deque([src])
        dirs = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]

        while q:
            r, c = q.popleft()
            for dr, dc, mv in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1 and dist[nr][nc] == -1:
                    dist[nr][nc]   = dist[r][c] + 1
                    parent[nr][nc] = ((r, c), mv)
                    q.append((nr, nc))

        return dist, parent

    def reconstruct(parent, dst):
        moves = []
        r, c  = dst
        while parent[r][c] is not None:
            (pr, pc), mv = parent[r][c]
            moves.append(mv)
            r, c = pr, pc
        moves.reverse()
        return ''.join(moves)

    key_points = [start] + cheeses + [goal]
    K          = len(key_points)
    IDX_START  = 0
    IDX_GOAL   = K - 1
    pair_dist = [[10**9] * K for _ in range(K)]
    pair_path = [[''   ] * K for _ in range(K)]

    for i, kp in enumerate(key_points):
        pair_dist[i][i] = 0
        pair_path[i][i] = ''
        dist_map, par_map = bfs_from(kp)
        for j, kp2 in enumerate(key_points):
            if i == j:
                continue
            r2, c2 = kp2
            if dist_map[r2][c2] != -1:
                pair_dist[i][j] = dist_map[r2][c2]
                pair_path[i][j] = reconstruct(par_map, kp2)

    if n_cheese == 0:
        return pair_path[IDX_START][IDX_GOAL]

    FULL_MASK = (1 << n_cheese) - 1
    INF       = 10**9
    dp      = [[INF] * n_cheese for _ in range(1 << n_cheese)]
    dp_prev = [[None] * n_cheese for _ in range(1 << n_cheese)]

    for i in range(n_cheese):
        ki   = i + 1          
        cost = pair_dist[IDX_START][ki]
        if cost < INF:
            mask       = 1 << i
            dp[mask][i] = cost
            dp_prev[mask][i] = (-1, -1)

    for mask in range(1, 1 << n_cheese):
        for i in range(n_cheese):
            if not (mask & (1 << i)):
                continue
            if dp[mask][i] == INF:
                continue
            ki = i + 1
            for j in range(n_cheese):
                if mask & (1 << j):
                    continue
                kj        = j + 1
                new_mask  = mask | (1 << j)
                new_cost  = dp[mask][i] + pair_dist[ki][kj]
                if new_cost < dp[new_mask][j]:
                    dp[new_mask][j]      = new_cost
                    dp_prev[new_mask][j] = (mask, i)

    best_cost       = INF
    best_last_cheese = -1
    for i in range(n_cheese):
        ki   = i + 1
        cost = dp[FULL_MASK][i] + pair_dist[ki][IDX_GOAL]
        if cost < best_cost:
            best_cost        = cost
            best_last_cheese = i

    if best_cost == INF:
        return ""

    order = []
    mask  = FULL_MASK
    ci    = best_last_cheese

    while ci != -1:
        order.append(ci)
        prev = dp_prev[mask][ci]
        if prev == (-1, -1):
            break
        prev_mask, prev_ci = prev
        mask = prev_mask
        ci   = prev_ci

    order.reverse()

    full_path = []

    first_ki    = order[0] + 1
    full_path.append(pair_path[IDX_START][first_ki])

    for idx in range(len(order) - 1):
        from_ki = order[idx]     + 1
        to_ki   = order[idx + 1] + 1
        full_path.append(pair_path[from_ki][to_ki])

    last_ki = order[-1] + 1
    full_path.append(pair_path[last_ki][IDX_GOAL])

    return ''.join(full_path)

if __name__ == "__main__":
    def run_maze(name, grid):
        rows, cols = len(grid), len(grid[0])
        path = solve_maze(grid)

        r, c = 0, 0
        move_map = {'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R': (0,1)}
        cheeses_needed = set()
        for rr in range(rows):
            for cc in range(cols):
                if grid[rr][cc] == 2:
                    cheeses_needed.add((rr, cc))

        cheeses_collected = set()
        steps = 0
        valid = True
        reason = ""

        for move in path:
            dr, dc = move_map[move]
            r, c = r + dr, c + dc
            steps += 1
            if not (0 <= r < rows and 0 <= c < cols):
                valid = False; reason = f"Out of bounds at step {steps}"; break
            if grid[r][c] == 1:
                valid = False; reason = f"Hit wall at ({r},{c}) step {steps}"; break
            if (r, c) in cheeses_needed:
                cheeses_collected.add((r, c))

        if valid:
            if r != rows-1 or c != cols-1:
                valid = False; reason = f"Did not reach goal, ended at ({r},{c})"
            elif cheeses_collected != cheeses_needed:
                missing = cheeses_needed - cheeses_collected
                valid = False; reason = f"Missing cheese at {missing}"

        status = f"✅ SOLVED in {steps} steps" if valid else f"❌ FAILED — {reason}"
        print(f"{name:30s}  {status}")
        if not valid:
            print(f"   Path: {path}")

    # 10 Training Mazes
    run_maze("1. No-cheese 3x3", [[0,0,0],[0,1,0],[0,0,0]])
    run_maze("2. Single cheese corridor", [[0,2,0],[0,0,0],[0,0,0]])
    run_maze("3. Two cheeses 4x4", [[0,0,0,0],[0,1,1,0],[0,2,0,0],[2,0,0,0]])
    run_maze("4. Three cheeses zigzag", [[0,0,0,0,0],[1,1,1,1,0],[2,0,0,0,0],[0,1,1,1,1],[0,2,0,2,0]])
    run_maze("5. Corner cheeses 5x5", [[0,0,0,0,2],[0,1,1,1,0],[0,1,0,1,0],[0,1,1,1,0],[2,0,0,0,0]])
    run_maze("6. Winding 6x6", [[0,1,0,0,0,0],[0,1,0,1,1,0],[0,0,0,1,0,0],[1,1,0,1,0,1],[0,0,0,0,2,0],[0,1,1,1,0,0]])
    run_maze("7. Dense cheese 5x5", [[0,2,0,2,0],[2,0,0,0,2],[0,0,1,0,0],[2,0,0,0,2],[0,2,0,2,0]])
    run_maze("8. Detour cheese 5x5", [[0,0,0,0,0],[1,1,1,1,0],[0,0,0,0,0],[0,1,1,1,1],[0,0,2,0,0]])
    run_maze("9. Larger 8x8", [[0,0,0,1,0,0,0,0],[0,1,0,1,0,1,1,0],[0,1,0,0,0,0,1,0],[0,1,1,1,1,0,1,0],[0,0,0,0,1,2,1,0],[1,1,1,0,1,0,0,0],[0,0,2,0,0,0,1,0],[0,0,1,1,1,0,0,0]])
    run_maze("10. Stress 10x10, 5 cheeses", [[0,0,0,0,0,0,0,0,0,0],[0,1,1,1,0,1,1,1,1,0],[0,1,0,0,0,0,0,0,1,0],[0,1,0,1,1,1,1,0,1,0],[0,0,0,1,2,0,1,0,0,0],[0,1,0,1,0,0,1,0,1,0],[0,1,0,0,0,1,1,0,1,0],[0,1,1,1,0,2,0,0,1,0],[0,0,0,0,0,1,1,1,1,0],[2,0,1,0,2,0,0,2,0,0]])
