from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "student_performance.csv"
OUTPUT_DIR = BASE_DIR / "output"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_FILE)
    numeric_columns = [
        "Study_Hours",
        "Attendance",
        "Assignment_Score",
        "Exam_Score",
    ]

    print("=== Student Performance Analysis ===")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print("\nDescriptive statistics:")
    print(df[numeric_columns].describe().round(2))

    avg_exam = df["Exam_Score"].mean()
    max_exam = df["Exam_Score"].max()
    min_exam = df["Exam_Score"].min()
    avg_attendance = df["Attendance"].mean()
    avg_study = df["Study_Hours"].mean()

    department_avg = df.groupby("Department")["Exam_Score"].mean().sort_values(ascending=False)
    correlation = df[numeric_columns].corr()

    print(f"\nAverage exam score: {avg_exam:.2f}")
    print(f"Highest exam score: {max_exam:.2f}")
    print(f"Lowest exam score: {min_exam:.2f}")
    print(f"Average attendance: {avg_attendance:.2f}%")
    print(f"Average study hours: {avg_study:.2f}")

    # 1. Bar chart
    plt.figure(figsize=(8, 5))
    department_avg.plot(kind="bar")
    plt.title("Average Exam Score by Department")
    plt.xlabel("Department")
    plt.ylabel("Average Exam Score")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "bar_chart_department_scores.png", dpi=160)
    plt.close()

    # 2. Scatter plot
    plt.figure(figsize=(8, 5))
    plt.scatter(df["Study_Hours"], df["Exam_Score"], alpha=0.8)
    plt.title("Study Hours vs. Exam Score")
    plt.xlabel("Study Hours")
    plt.ylabel("Exam Score")
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "scatter_study_vs_exam.png", dpi=160)
    plt.close()

    # 3. Heatmap using Matplotlib (imshow)
    fig, ax = plt.subplots(figsize=(8, 6))
    matrix = correlation.to_numpy()
    image = ax.imshow(matrix, cmap="viridis", vmin=-1, vmax=1)
    fig.colorbar(image, ax=ax, label="Correlation")
    ax.set_xticks(np.arange(len(numeric_columns)), labels=numeric_columns, rotation=35, ha="right")
    ax.set_yticks(np.arange(len(numeric_columns)), labels=numeric_columns)
    ax.set_title("Correlation Heatmap of Numerical Features")

    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            ax.text(col, row, f"{matrix[row, col]:.2f}", ha="center", va="center")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "heatmap_correlations.png", dpi=160)
    plt.close(fig)

    top_department = department_avg.index[0]
    study_exam_corr = correlation.loc["Study_Hours", "Exam_Score"]
    attendance_exam_corr = correlation.loc["Attendance", "Exam_Score"]

    summary = f"""Student Performance Analysis — Generated Output

Dataset size: {df.shape[0]} rows x {df.shape[1]} columns

Key statistics
--------------
Average exam score: {avg_exam:.2f}
Highest exam score: {max_exam:.2f}
Lowest exam score: {min_exam:.2f}
Average attendance: {avg_attendance:.2f}%
Average study hours: {avg_study:.2f}

Average exam score by department
--------------------------------
{department_avg.round(2).to_string()}

Insights
--------
1. {top_department} has the highest average exam score in this sample.
2. The correlation between study hours and exam score is {study_exam_corr:.2f}.
3. The correlation between attendance and exam score is {attendance_exam_corr:.2f}.
4. The generated bar chart, scatter plot, and heatmap provide visual support for these observations.

Files generated
---------------
- bar_chart_department_scores.png
- scatter_study_vs_exam.png
- heatmap_correlations.png
"""
    (OUTPUT_DIR / "analysis_summary.txt").write_text(summary, encoding="utf-8")
    print("\nAnalysis complete. Check the output/ folder for charts and the generated summary.")


if __name__ == "__main__":
    main()
