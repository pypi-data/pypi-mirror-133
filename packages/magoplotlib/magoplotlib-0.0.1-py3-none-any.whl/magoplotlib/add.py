import datetime


def add_timestamp(fig, loc="bottom right", fmt=None, dt=None, tz=None, fontdict=None, **kwargs) -> None:
    """add timestamp on figure

    Parameters
    ----------
    fig : figure
    loc : str
        Positon of timestamp. bottom or top. left, center or right.
        Default is "bottom right".
    fmt : str, Optional
        format. with time. Default is "Generated at %Y-%m-%dT%H:%M:%S"
    dt : datetime.datetime, Optional.
    tz: Timezone object, Optional.
    fontdict : dict, optional
        pass to
    kwargs : dict, Optional
        Text Property.
    """
    if loc == "top left":
        y = 1
        x = 0
        va = "top"
        ha = "left"
    elif loc == "top center":
        y = 1
        x = 0.5
        va = "top"
        ha = "center"
    elif loc == "top right":
        y = 1
        x = 1
        va = "top"
        ha = "right"
    elif loc == "bottom left":
        y = 0
        x = 0
        va = "bottom"
        ha = "left"
    elif loc == "bottom center":
        y = 0
        x = 0.5
        va = "bottom"
        ha = "center"
    elif loc == "bottom right":
        y = 0
        x = 1
        va = "bottom"
        ha = "right"
    else:
        raise ValueError("keyward loc is not expected value")

    if fmt is None:
        fmt = "Generated at %Y-%m-%dT%H:%M:%S"
    if dt is None:
        dt = datetime.datetime.now(tz)

    fig.text(x, y, dt.strftime(fmt), ha=ha, va=va, fontdict=fontdict, **kwargs)
