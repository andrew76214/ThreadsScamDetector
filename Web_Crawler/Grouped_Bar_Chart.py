import matplotlib.pyplot as plt
import numpy as np

# Data preparation
categories = ['work', 'gambling', 'dating', 'investment']
# Updating the data with new methods and completely different values
methods = [
    'Llama3-TAIDE-LX-8B-Chat-Alpha1 + few-shot learning',
    'Breeze-7B-Instruct-v1_0 + few-shot learning',
    'Llama3-TAIDE-LX-8B-Chat-Alpha1 + finetune',
    'Breeze-7B-Instruct-v1_0 + finetune',
    'Llama3-TAIDE-LX-8B-Chat-Alpha1 + agentic AI',
    'Breeze-7B-Instruct-v1_0 + agentic AI'
]

data = [
    [0.629, 0.904, 0.759, 0.502],  # Few-shot learning for Llama3-TAIDE
    [0.671, 0.890, 0.744, 0.521],  # Few-shot learning for Breeze
    [0.732, 0.845, 0.772, 0.462],  # Finetune for Llama3-TAIDE
    [0.714, 0.812, 0.751, 0.488],  # Finetune for Breeze
    [0.790, 0.923, 0.820, 0.545],  # Agentic AI for Llama3-TAIDE
    [0.748, 0.902, 0.801, 0.532]   # Agentic AI for Breeze
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
ax.set_ylim(0.4, 1.0)

# Show the plot
plt.tight_layout()
plt.show()
