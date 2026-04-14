import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

# Set Chinese font to avoid garbled text
plt.rcParams['font.family'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False

# Read the Excel file
file_path = "Kano_分析結果.xlsx"
strict_df = pd.read_excel(file_path, index_col=0)

# Extract columns needed for plotting
plot_df = strict_df[["SI", "DSI", "Result"]].copy()

# Define color and label mapping for each Kano result category
color_map = {
    'A': ('green', 'A: Attractive'),
    'O': ('blue', 'O: One-dimensional'),
    'M': ('red', 'M: Must-be'),
    'I': ('gray', 'I: Indifferent'),
    'R': ('orange', 'R: Reverse'),
    'Q': ('purple', 'Q: Questionable')
}

# Find categories that actually appear in the data
present_categories = plot_df["Result"].unique()

# Create the figure
plt.figure(figsize=(20, 18))  # Adjust size as needed

# Plot data points and labels
for idx, row in plot_df.iterrows():
    color, _ = color_map.get(row["Result"], ('black', 'Unknown'))
    plt.scatter(row["SI"], row["DSI"], color=color)
    if "和其他常用的學術軟體連結，如Zotero" in row.name:
        plt.text(row["SI"] + 0.003, row["DSI"] - 0.008, idx, fontsize=12)
    elif "根據您的提問，推薦相似或相關問題" in row.name:
        plt.text(row["SI"] + 0.003, row["DSI"] - 0.002, idx, fontsize=12)
    else:
        plt.text(row["SI"] + 0.003, row["DSI"] - 0.005, idx, fontsize=12)

# Calculate quadrant divider position: midpoint between O max and I min
si_o_max = plot_df[plot_df["Result"] == "O"]["SI"].max()
si_i_min = plot_df[plot_df["Result"] == "I"]["SI"].min()
si_axis = (si_o_max + si_i_min) / 2

dsi_o_max = plot_df[plot_df["Result"] == "O"]["DSI"].max()
dsi_i_min = plot_df[plot_df["Result"] == "I"]["DSI"].min()
dsi_axis = (dsi_o_max + dsi_i_min) / 2

# Draw quadrant divider lines
plt.axvline(x=si_axis, color='black', linestyle='--', linewidth=1)
plt.axhline(y=dsi_axis, color='black', linestyle='--', linewidth=1)


# Set axis limits to prevent text from overflowing
plt.xlim(plot_df["SI"].min() - 0.02, plot_df["SI"].max() + 0.05)
plt.ylim(plot_df["DSI"].min() - 0.05, plot_df["DSI"].max() + 0.05)

# Add axis labels and title
plt.xlabel("Satisfaction Increment (SI)")
plt.ylabel("Dissatisfaction Decrement (DSI)")
plt.title("Kano Model Feature Distribution")

# Define custom legend order
custom_order = ['M', 'O', 'A', 'I', 'R', 'Q']

# Filter to only present categories and generate legend in order
legend_handles = [
    patches.Patch(color=color_map[code][0], label=color_map[code][1])
    for code in custom_order if code in plot_df["Result"].unique()
]

plt.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1, 0.5))

# Adjust spacing between plot and legend
# plt.tight_layout(rect=[0, 0, 0.85, 1])

# Save and display the figure

plt.savefig("kano_plot.png", dpi=300, bbox_inches='tight')
plt.show()
