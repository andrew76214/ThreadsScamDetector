import matplotlib.pyplot as plt
import numpy as np

# Data preparation
categories = ['work', 'gambling', 'dating', 'investment']
# Updating the data with new methods and completely different values
methods = [
    'Llama3-TAIDE-LX-8B-Chat-Alpha1 + few-shot learning',
    'Breeze-7B-Instruct-v1_0 + few-shot learning',
    'Qwen2.5-1.5B-Instruct + few-shot learning',
    'Llama3-TAIDE-LX-8B-Chat-Alpha1 + finetune',
    'Breeze-7B-Instruct-v1_0 + finetune',
    'Qwen2.5-1.5B-Instruct + finetune'
]

data = [
    [0.629, 0.904, 0.759, 0.502],  # Few-shot learning for Llama3-TAIDE
    [0.689, 0.764, 0.720, 0.530],  # Few-shot learning for Breeze
    [0.546, 0.729, 0.612, 0.360],  # Few-shot learning for qwen
    [0.732, 0.845, 0.772, 0.462],  # Finetune for Llama3-TAIDE
    [0.717, 0.810, 0.694, 0.420],  # Finetune for Breeze
    [0.747, 0.751, 0.649, 0.366]   # Finetune for qwen
]

# Plot configuration for the new data
x = np.arange(len(categories))  # X axis positions for categories
width = 0.12  # Adjusted width for more groups

# Creating the plot
fig, ax = plt.subplots(figsize=(12, 7))
for i, method_data in enumerate(data):
    ax.bar(x + i * width, method_data, width, alpha=0.7, label=methods[i])

# Adding labels and title
ax.set_xlabel('Categories', fontsize=12)
ax.set_ylabel('F-1 Scores', fontsize=12)
ax.set_title('Performance Comparison Across Methods and Categories', fontsize=14)
ax.set_xticks(x + width * (len(methods) / 2 - 0.5))
ax.set_xticklabels(categories, fontsize=11)
ax.legend(title='Methods', fontsize=10, title_fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Setting Y-axis limit
ax.set_ylim(0.35, 1.0)

# Show the plot
plt.tight_layout()
plt.show()
