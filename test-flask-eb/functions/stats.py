from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def gen_stats(width_px, height_px):
    num_students = 10
    courses_completed = np.random.randint(0, 11, size=num_students)
    videos_viewed = np.random.randint(0, 11, size=num_students)
    assignments_completed = np.random.randint(0, 11, size=num_students)
    dpi = 100
    width_inches = width_px / dpi
    height_inches = height_px / dpi
    fig, ax = plt.subplots(figsize=(width_inches, height_inches))
    bar_width = 0.25
    index = np.arange(num_students)

    ax.bar(index - bar_width, courses_completed, bar_width, label='Courses')
    ax.bar(index, videos_viewed, bar_width, label='Videos')
    ax.bar(index + bar_width, assignments_completed, bar_width, label='Assignments')
    ax.set_title('Student Progress')
    ax.set_xlabel('Students')
    ax.set_ylabel('Number Completed')
    ax.set_xticks(index)
    ax.set_xticklabels([str(i) for i in range(1, num_students + 1)])
    ax.set_yticks(np.arange(0, 11))
    ax.legend()
    ax.grid(True)

    img = io.BytesIO()
    fig.savefig(img, format='png', dpi=dpi)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)

    return render_template('index.html', plot_url=plot_url)
