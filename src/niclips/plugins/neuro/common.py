"""Generic views that can be used for all neuroimage modalities."""

from nilearn import plotting

from niclips.core.factory import ViewFactory
from niclips.typing import StrPath


@ViewFactory.register()
def multi_view(
    img: StrPath,
    output_path: StrPath,
    *,
    overlay: StrPath | None = None,
    colorbar: bool = False,
    cmap: str = "gray",
    **kwargs,
) -> None:
    """Construct multi-view image panel.

    See https://nilearn.github.io/stable/modules/generated/nilearn.plotting.plot_stat_map.html
    for additional arguments
    """
    plotting.plot_stat_map(
        stat_map_img=img if overlay is None else overlay,
        bg_img=img if overlay else None,
        output_file=output_path,
        colorbar=colorbar,
        cmap=cmap,
        display_mode="ortho",
        **kwargs,
    )
