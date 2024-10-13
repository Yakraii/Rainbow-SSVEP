import numpy as np
import matplotlib.pyplot as plt

# 示例数据
groups = 5
bars_per_group = 5
labels = ['sub 1', 'sub 2', 'sub 3', 'sub 4', 'sub 5']
modelsName = ['RandomForestClassifier', 'Perceptron', 'KNeighborsClassifier', 'SVC', 'DecisionTreeClassifier']

# 为了简化，这里使用随机数据
np.random.seed(42)  # 使随机结果可重复
data = np.random.randint(90, 100, size=(groups, bars_per_group))

# 设置柱子的位置和宽度
barWidth = 0.15
r = np.arange(bars_per_group)  # 柱子位置

# 绘制柱状图
for i in range(groups):
    plt.bar(r + i*barWidth, data[i], color=np.random.rand(3,), width=barWidth, edgecolor='white', label=f'{modelsName[i]}')

# 添加标签，标题等
plt.xlabel('subjects', fontweight='bold')
plt.xticks([r + barWidth for r in range(bars_per_group)], labels)
plt.title('5 subject with 5 Classifier')
plt.legend()

# 显示图形
plt.show()
