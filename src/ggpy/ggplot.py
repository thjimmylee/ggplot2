from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Tuple

import matplotlib

# Ensure a non-interactive backend for headless environments
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def aes(**kwargs: str) -> Dict[str, str]:
    """
    Define aesthetic mappings between column names and visual properties.
    """
    return kwargs


class GGPlot:
    """
    Minimal ggplot-like interface using pandas DataFrames and matplotlib.
    Supports dot-chaining only (no operator overloading).
    """

    def __init__(self, data: pd.DataFrame, mapping: Optional[Dict[str, str]] = None) -> None:
        self.data = self._coerce_dataframe(data)
        self.mapping: Dict[str, str] = mapping or {}
        self.geoms: List[Tuple[str, Dict[str, Any]]] = []
        self.labels: Dict[str, str] = {}
        self._theme: Optional[str] = None

    @staticmethod
    def _coerce_dataframe(data: Any) -> pd.DataFrame:
        if isinstance(data, pd.DataFrame):
            return data.copy()
        return pd.DataFrame(data)

    def geom_point(self, **kwargs: Any) -> "GGPlot":
        self.geoms.append(("point", kwargs))
        return self

    def geom_line(self, **kwargs: Any) -> "GGPlot":
        self.geoms.append(("line", kwargs))
        return self

    def theme_minimal(self) -> "GGPlot":
        self._theme = "minimal"
        return self

    def labs(self, **kwargs: str) -> "GGPlot":
        # Only record non-empty labels
        for key, value in kwargs.items():
            if value is not None:
                self.labels[key] = value
        return self

    def show(self):
        fig, _ = self._render()
        return fig

    def save(self, filename: str, **kwargs: Any) -> str:
        fig, _ = self._render()
        fig.savefig(filename, **kwargs)
        plt.close(fig)
        return filename

    # Internal helpers
    def _render(self):
        self._validate_required_mapping()
        fig, ax = plt.subplots()

        if self._theme == "minimal":
            self._apply_theme_minimal(ax)

        x = self._get_column("x")
        y = self._get_column("y")
        color = self._get_column("color")
        if color is None:
            color = self._get_column("colour")

        for geom, params in self.geoms or [("point", {})]:
            if geom == "point":
                ax.scatter(x, y, c=color if color is not None else None, **params)
            elif geom == "line":
                ax.plot(x, y, **params)

        # Apply labels
        if "title" in self.labels:
            ax.set_title(self.labels["title"])
        ax.set_xlabel(self.labels.get("x", self.mapping.get("x", "")))
        ax.set_ylabel(self.labels.get("y", self.mapping.get("y", "")))

        fig.tight_layout()
        return fig, ax

    def _get_column(self, key: str):
        column_name = self.mapping.get(key)
        if column_name is None:
            return None
        if column_name not in self.data.columns:
            raise KeyError(f"Column '{column_name}' not found in data.")
        return self.data[column_name]

    def _validate_required_mapping(self) -> None:
        for key in ("x", "y"):
            if key not in self.mapping:
                raise ValueError(f"Mapping must include '{key}'.")
            if self.mapping[key] not in self.data.columns:
                raise ValueError(f"Mapping for '{key}' refers to missing column '{self.mapping[key]}'.")

    @staticmethod
    def _apply_theme_minimal(ax) -> None:
        ax.set_facecolor("white")
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        ax.grid(True, color="#eaeaea")
        ax.tick_params(colors="#444444")
        ax.title.set_color("#222222")
        ax.xaxis.label.set_color("#222222")
        ax.yaxis.label.set_color("#222222")


def ggplot(data: Any, mapping: Optional[Dict[str, str]] = None) -> GGPlot:
    return GGPlot(data, mapping)
