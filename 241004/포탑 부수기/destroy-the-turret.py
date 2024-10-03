from collections import deque
import copy

def make_list(n, m, arr, cnt):
    attack_list = []
    for i in range(n):
        for j in range(m):
            if arr[i][j] > 0:
                attack_list.append([arr[i][j], cnt[i][j], i + j, j])

    return attack_list
            
def select_attack(attack_list):
    now = copy.deepcopy(attack_list)
    now.sort(key=lambda x : (x[0], -x[1], -x[2], -x[3]))
    
    return now

def razor(n, m, arr, pos1, pos2, s):
    dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    q = deque()
    path = []
    path.append(pos1)
    q.append(path)
    
    visited = [[False] * m for _ in range(n)]
    visited[pos1[0]][pos1[1]] = True

    while q:
        now = q.popleft()
        now_attack = now[-1]

        for i in range(4):
            cpy = now.copy()
            nx = now_attack[0] + dir[i][0]
            ny = now_attack[1] + dir[i][1]

            if nx < 0:
                nx = n - 1
            if ny < 0:
                ny = m - 1
            if nx >= n:
                nx = 0
            if ny >= m:
                ny = 0

            if arr[nx][ny] <= 0 or visited[nx][ny]:
                continue
            if [nx, ny] == pos2:
                arr[nx][ny] -= s
                for p in range(1, len(cpy)):
                    ppos = cpy[p]
                    arr[ppos[0]][ppos[1]] -= (s // 2)

                for ii in range(n):
                    for jj in range(m):
                        if [ii, jj] not in cpy and [ii, jj] != pos2 and arr[ii][jj] > 0:
                            arr[ii][jj] += 1
                # print('razor', *arr, sep='\n')
                return arr

            cpy.append([nx, ny])
            visited[nx][ny] = True
            q.append(cpy)

    return bomb(n, m, arr, pos1, pos2, s)

def bomb(n, m, arr, pos1, pos2, s):
    path = []
    path.append(pos1)

    dir = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for i in range(8):
        nx = pos2[0] + dir[i][0]
        ny = pos2[1] + dir[i][1]

        if nx < 0:
            nx = n - 1
        if ny < 0:
            ny = m - 1
        if nx >= n:
            nx = 0
        if ny >= m:
            ny = 0

        if [nx, ny] != pos2 and arr[nx][ny] > 0:
            arr[nx][ny] -= (s // 2)
            path.append([nx, ny])

    arr[pos2[0]][pos2[1]] -= s

    for i in range(n):
        for j in range(m):
            if [i, j] not in path and [i, j] != pos2 and arr[i][j] > 0:
                arr[i][j] += 1
    # print('bomb', *arr, sep="\n")
    return arr


n, m, k = map(int, input().split())

arr = []
cnt = [[-1] * m for _ in range(n)]
# 공격력, 공격 시점, 행과 열 합, 열 값
attack_list = []
for _ in range(n):
    arr.append(list(map(int, input().split())))

for i in range(k):
    attack_list = copy.deepcopy(make_list(n, m, arr, cnt))

    if len(attack_list) == 1:
        break
    
    weak = select_attack(attack_list)[0]
    pos1 = [weak[2] - weak[3], weak[3]]
    strong = select_attack(attack_list)[-1]
    pos2 = [strong[2] - strong[3], strong[3]]

    # print(i, pos1, pos2)
    
    arr[pos1[0]][pos1[1]] += (n + m)
    cnt[pos1[0]][pos1[1]] = i

    # print('start', *arr, sep='\n')
    arr = copy.deepcopy(razor(n, m, arr, pos1, pos2, arr[pos1[0]][pos1[1]]))

ans = 0
for i in range(n):
    for j in range(m):
        ans = max(ans, arr[i][j])

print(ans)