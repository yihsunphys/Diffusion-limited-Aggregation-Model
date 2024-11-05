import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# DLA 模型參數
grid_size = 101  # 方格的大小
center = grid_size // 2  # 中心位置
steps = 5000  # 每個粒子運動的最大步數
cluster_radius = 1  # 聚集半徑

# 初始化網格，中心設為已聚集的“種子”點
grid = np.zeros((grid_size, grid_size), dtype=bool)
grid[center, center] = True

# 設定粒子的起始位置，通常從聚集區域外的隨機位置開始
def random_start(radius):
    theta = 2 * np.pi * np.random.rand()
    x = int(center + (radius + 1) * np.cos(theta))
    y = int(center + (radius + 1) * np.sin(theta))
    return x, y

# 初始化粒子的位置和路徑
x, y = random_start(cluster_radius)
path = [(x, y)]  # 路徑列表

# 設定動畫
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, grid_size)
ax.set_ylim(0, grid_size)
ax.axis('off')  # 關閉坐標軸

# 初始圖像
image = ax.imshow(grid, cmap='binary', interpolation='nearest')
particle_path, = ax.plot([], [], 'r-', lw=1)  # 顯示粒子的運動軌跡
particle, = ax.plot([], [], 'ro', markersize=2)  # 顯示粒子的當前位置

# 初始化動畫
def init():
    image.set_data(grid)
    particle_path.set_data([], [])
    particle.set_data([], [])
    return image, particle_path, particle

# 更新動畫
def update(frame):
    global x, y, path, cluster_radius
    
    # 粒子隨機選擇一個方向（上下左右）
    x += np.random.choice([-1, 0, 1])
    y += np.random.choice([-1, 0, 1])

    # 如果粒子走到邊界外，重新開始
    if x <= 1 or x >= grid_size - 2 or y <= 1 or y >= grid_size - 2:
        x, y = random_start(cluster_radius)
        path = [(x, y)]
        return image, particle_path, particle

    # 記錄粒子的位置
    path.append((x, y))
    
    # 檢查是否接觸到已聚集的結構
    if grid[x+1, y] or grid[x-1, y] or grid[x, y+1] or grid[x, y-1]:
        grid[x, y] = True  # 粒子聚集
        cluster_radius = max(cluster_radius, np.sqrt((x - center)**2 + (y - center)**2))  # 更新聚集半徑
        x, y = random_start(cluster_radius)  # 生成新粒子
        path = [(x, y)]  # 重置路徑
    else:
        # 更新粒子的路徑和當前位置
        x_path, y_path = zip(*path)
        particle_path.set_data(x_path, y_path)
        particle.set_data(x, y)

    # 更新網格顯示已聚集的結構
    image.set_data(grid)
    return image, particle_path, particle

# 建立動畫，每秒更新一次（1000ms）
ani = FuncAnimation(fig, update, frames=5000, init_func=init, interval=100, blit=True)
plt.show()
