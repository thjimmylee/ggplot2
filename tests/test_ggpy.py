import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.use("Agg")

from ggpy import GGPlot, aes, ggplot


def sample_df():
    return pd.DataFrame(
        {
            "x": [1, 2, 3],
            "y": [1, 3, 2],
            "color": [0.1, 0.5, 0.9],
        }
    )


def test_chaining_returns_self_and_records_geoms():
    df = sample_df()
    plot = ggplot(df, aes(x="x", y="y"))
    returned = plot.geom_point()
    assert returned is plot
    assert plot.geoms[0][0] == "point"


def test_geom_line_drawn():
    df = sample_df()
    fig = ggplot(df, aes(x="x", y="y")).geom_line().show()
    ax = fig.axes[0]
    assert len(ax.lines) == 1
    plt.close(fig)


def test_labs_sets_titles_and_axes_labels():
    df = sample_df()
    fig = (
        ggplot(df, aes(x="x", y="y"))
        .geom_point()
        .labs(title="My Plot", x="X label", y="Y label")
        .show()
    )
    ax = fig.axes[0]
    assert ax.get_title() == "My Plot"
    assert ax.get_xlabel() == "X label"
    assert ax.get_ylabel() == "Y label"
    plt.close(fig)


def test_theme_minimal_hides_top_and_right_spines():
    df = sample_df()
    fig = ggplot(df, aes(x="x", y="y")).geom_point().theme_minimal().show()
    ax = fig.axes[0]
    assert not ax.spines["top"].get_visible()
    assert not ax.spines["right"].get_visible()
    plt.close(fig)


def test_color_mapping_used_for_points():
    df = sample_df()
    fig = ggplot(df, aes(x="x", y="y", color="color")).geom_point().show()
    collection = fig.axes[0].collections[0]
    np.testing.assert_allclose(collection.get_array(), df["color"].to_numpy())
    plt.close(fig)


def test_save_creates_file(tmp_path):
    df = sample_df()
    output = tmp_path / "plot.png"
    path = ggplot(df, aes(x="x", y="y")).geom_point().save(output)
    assert path == str(output) or path == output
    assert output.exists()
    assert output.stat().st_size > 0
