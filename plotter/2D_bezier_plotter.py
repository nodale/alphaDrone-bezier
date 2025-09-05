import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from scipy.interpolate import CubicSpline

def plot_splines_from_txt(fig, filename):
    curves = []
    current_points = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                if current_points:
                    curves.append(current_points)
                    current_points = []
            else:
                x, y = map(float, line.split())
                current_points.append((x, y))
        if current_points:
            curves.append(current_points)

    for i, points in enumerate(curves, start=1):
        points = np.array(points)
        t = np.arange(len(points))
        x, y = points[:, 0], points[:, 1]

        cs_x = CubicSpline(t, x)
        cs_y = CubicSpline(t, y)

        t_fine = np.linspace(0, len(points)-1, 200)
        x_fine, y_fine = cs_x(t_fine), cs_y(t_fine)

        fig.add_trace(go.Scatter(x=x_fine, y=y_fine,
                                 mode="lines",
                                 name=f"curve{i} spline"))

        #fig.add_trace(go.Scatter(x=x, y=y,
        #                         mode="markers+text",
        #                         text=[f"p{j}" for j in range(len(points))],
        #                         textposition="top center",
        #                         name=f"curve{i} points"))

    return fig

df = pd.read_csv("b.txt", 
                 sep=r"\s+",   
                 header=None)

df.columns = ["x1","y1","z1","x2","y2","z2","x3","y3","z3","t"]

print(df.head())

time = df.index 

fig = go.Figure()

## Trajectory 1 (point path)
#fig.add_trace(go.Scatter3d(
#    x=df["x1"], y=df["y1"], z=df["z1"],
#    mode="lines+markers", name="Trajectory 1"
#))

#Trajectory 2 (point path)
fig.add_trace(go.Scatter(
    x=df["x2"], y=df["y2"],
    mode="lines", name="Trajectory 2"
))
#
scale = 0.5
for i in range(len(df)):
    fig.add_trace(go.Scatter(
        x=[df["x2"][i], df["x2"][i] + df["x3"][i] * scale],
        y=[df["y2"][i], df["y2"][i] + df["y3"][i] * scale],
        mode="lines+markers",
        line=dict(color="red", width=1),
        marker=dict(size=0.4),
    ))

plot_splines_from_txt(fig, 'bezier.txt')

fig.update_layout(
    title="2D Trajectory along Bezier Curves",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
    )
)

fig.show()
