import matplotlib.pyplot as plt
import numpy as np

# Data preparation
categories = ['work', 'gambling', 'dating', 'investment']
methods = ['model 1 + method 1', 'model 1 + method 2', 'model 2 + method 1', 'model 2 + method 2']

data = [
    [0.629, 0.904, 0.759, 0.502],  # model 1 + method 1
    [0.702, 0.829, 0.735, 0.428],  # model 1 + method 2
    [0.702, 0.829, 0.735, 0.428],  # model 2 + method 1
    [0.702, 0.502, 0.735, 0.428]   # model 2 + method 2
]

# Plot configuration
x = np.arange(len(categories))  # X axis positions for categories
width = 0.2  # Width of each bar

# Creating the plot
fig, ax = plt.subplots(figsize=(10, 6))
for i, method_data in enumerate(data):
    ax.bar(x + i * width, method_data, width, label=methods[i])

# Adding labels and title
ax.set_xlabel('Categories', fontsize=12)
ax.set_ylabel('Values', fontsize=12)
ax.set_title('Comparison of Model and Method Performance Across Categories', fontsize=14)
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(categories, fontsize=11)
ax.legend(title='Model + Method', fontsize=10, title_fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()
