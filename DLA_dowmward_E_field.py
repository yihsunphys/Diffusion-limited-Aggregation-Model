import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

# DLA 模型參數
grid_size = 301  # 方格的大小
center = grid_size // 2  # 中心位置
steps = 5000  # 粒子運動的總步數
cluster_radius = 1  # 聚集半徑

# 電場參數（方向偏向正X軸和正Y軸）
E_x, E_y = 1, 0

# 初始化網格，中心設為已聚集的“種子”點
grid = np.zeros((grid_size, grid_size), dtype=bool)
grid[center, center] = True

# 自訂配色：黑色背景和黃色結構
cmap = ListedColormap(['black', 'yellow'])

# 設定粒子的起始位置，通常從聚集區域外的隨機位置開始
def random_start(radius):
    theta = 2 * np.pi * np.random.rand()
    x = int(center + (radius + 1) * np.cos(theta))
    y = int(center + (radius + 1) * np.sin(theta))
    return x, y

# 粒子進行隨機行走，直到它聚集在已經存在的結構上
def random_walk():
    global cluster_radius
    x, y = random_start(cluster_radius)
    
    for _ in range(steps):
        # 基於電場的偏移機率
        move_probs = [
            (1 + E_x) / 4,  # 向右
            (1 - E_x) / 4,  # 向左
            (1 + E_y) / 4,  # 向上
            (1 - E_y) / 4   # 向下
        ]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        move = directions[np.random.choice(4, p=move_probs)]
        x += move[0]
        y += move[1]

        # 如果粒子走到邊界外，重新開始
        if x <= 1 or x >= grid_size - 2 or y <= 1 or y >= grid_size - 2:
            x, y = random_start(cluster_radius)
            continue
        
        # 檢查四周是否有聚集的粒子
        if grid[x+1, y] or grid[x-1, y] or grid[x, y+1] or grid[x, y-1]:
            grid[x, y] = True  # 聚集
            cluster_radius = max(cluster_radius, np.sqrt((x - center)**2 + (y - center)**2))  # 更新聚集半徑
            break

# 設定動畫
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, grid_size)
ax.set_ylim(0, grid_size)
ax.axis('off')  # 關閉坐標軸

# 初始圖像
image = ax.imshow(grid, cmap=cmap, interpolation='nearest')

def update(frame):
    random_walk()  # 執行隨機行走
    image.set_data(grid)  # 更新網格
    return [image]

# 建立動畫
ani = FuncAnimation(fig, update, frames=1000, interval=0.1, blit=True)

plt.show()
