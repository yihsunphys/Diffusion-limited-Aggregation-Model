import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

# 設定初始條件
line_length = 10  # 初始直線長度
max_depth = 7  # 最大迭代深度
displacement_factor = 8.0  # 偏移量因子
base_branch_length = 3.0  # 初始分支長度

# 從白色到較深的藍色過渡顏色
colors = LinearSegmentedColormap.from_list("white_to_blue", ["white", "#87CEEB", "blue"], N=256)

# 初始線段，將每個線段加上深度信息
segments = [((0, 0), (0, line_length), 0)]  # 初始直線，深度是0
all_segments = [segments]  # 用於保存每層線段的歷史記錄

# 初始化每次迭代生成新分支
def iterate_segments(segments, depth):
    branch_length = base_branch_length * (0.8 ** depth)  # 分支長度逐漸縮短
    new_segments = []
    for start, end, d in segments:  # 這裡的 d 是當前的深度
        # 計算隨機分支點
        t = np.random.uniform(0.2, 0.8)  # 隨機比例 t (0 ~ 1)
        branch_x = start[0] + t * (end[0] - start[0])
        branch_y = start[1] + t * (end[1] - start[1])

        # 偏移量（在 X 軸方向隨機偏移）
        offset = displacement_factor * np.random.uniform(-1, 1)
        branch_point = (branch_x + offset, branch_y)

        # 生成原始兩段，並記錄當前的深度
        new_segments.append((start, branch_point, d))  # 分支的深度增加
        new_segments.append((branch_point, end, d))

        # 根據深度減少生成新分支的機率
        branch_probability =  1 - 0.1 * depth**1.33  # 隨著深度增加，分支的機率逐漸減少

        # 生成額外的分支（確保固定長度，方向隨機）
        if np.random.random() < branch_probability:  # 根據機率決定是否生成額外分支
            random_angle = np.random.uniform(1.2 * np.pi, 1.8 * np.pi)  # 隨機角度 (0 ~ 2π)
            extra_offset_x = branch_length * np.cos(random_angle)
            extra_offset_y = branch_length * np.sin(random_angle)
            extra_branch_end = (branch_point[0] + extra_offset_x, branch_point[1] + extra_offset_y)
            new_segments.append((branch_point, extra_branch_end, d + 1))  # 新增額外分支，深度也增加

    return new_segments

# 設定圖像
fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')

def update(depth):
    global segments, displacement_factor

    ax.clear()  # 清除之前的圖像
    ax.set_facecolor("black")
    ax.set_xlim(-line_length / 2, line_length / 2)
    ax.set_ylim(0, line_length)
    ax.axis('off')  # 隱藏坐標軸
    
    # 每一層新增分支
    if depth == len(all_segments):
        new_segments = iterate_segments(segments, depth)
        segments = new_segments  # 更新當前的線段
        all_segments.append(new_segments)  # 保存當前線段到歷史記錄

    # 繪製當前新線段，並且每次迭代都使用不同的顏色
    for segment in all_segments[depth]:
        start, end, segment_depth = segment  # 解構線段的起點、終點和深度
        color = colors(segment_depth / max_depth)  # 根據分支的深度選擇顏色
        
        # 根據深度來調整線條寬度，深度越大，線條越細
        line_width = 3 - segment_depth * 0.4  # 設定最小寬度為 0.5
        
        x_vals = [start[0], end[0]]
        y_vals = [start[1], end[1]]
        ax.plot(x_vals, y_vals, color=color, lw=line_width, alpha=1.0)

    # 添加迭代次數文本
    ax.text(0, line_length + 1, f"Iteration: {depth + 1}", color="white", 
            fontsize=16, ha="center", va="bottom", weight="bold")

    # 減少偏移量，讓分支更細緻
    if depth == len(all_segments) - 1:
        displacement_factor *= 0.5

# 創建動畫
ani = FuncAnimation(fig, update, frames=max_depth, interval=1000, repeat=False)

# 保存動畫為 GIF
ani.save("branching_animation_with_decreasing_branch_probability.gif", writer='pillow', fps=1)

plt.show()
