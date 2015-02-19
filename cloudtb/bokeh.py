import numpy as np
import pandas as pd
from bokeh.models import LinearAxis, Range1d
from bokeh.palettes import brewer
from scipy import stats
import colorsys


def get_hex(color):
    color = tuple(int(n * 255) for n in color)
    return ('#' + '{:02x}' * 3).format(*color)


def get_colors(num_colors, hex=False):
    colors = []
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i / 360
        lightness = (50 + np.random.rand() * 10) / 100
        saturation = (90 + np.random.rand() * 10) / 100
        color = colorsys.hls_to_rgb(hue, lightness, saturation)
        if hex:
            color = get_hex(color)
        colors.append(color)
    return colors


def get_bins(x, y, bins):
    '''Put data into bins'''
    prev = 0
    assert len(x) == len(y)
    if len(y) <= bins:
        yield x, y
        raise StopIteration
    for i in range(len(y) // bins, len(y) - 1, len(y) // bins):
        yield x[prev:i], y[prev:i]
        prev = i
    if prev < len(x) - 1:
        yield x[prev:], y[prev:]


def linear_fit(x, y, bins=None):
    '''Return the linear variability in a number of bins'''
    if bins is None:
        # A = np.vstack([x, np.ones(len(x))]).T
        # m, c = np.linalg.lstsq(A, y)[0]
        m, c, r_value, p_value, std_err = stats.linregress(x, y)
        return m * x + c
    else:
        data = []
        for bx, by in get_bins(x, y, bins):
            data.append(linear_fit(bx, by))
        return np.concatenate(data)


def mean_fit(x, y, bins=None):
    if bins is None:
        return np.mean(x), np.mean(y)
    else:
        dx = []
        dy = []
        for bx, by in get_bins(x, y, bins):
            bx, by = mean_fit(bx, by)
            dx.append(bx)
            dy.append(by)
        return np.array(dx), np.array(dy)


def linear_std(x, y, bins, line=None):
    '''Returns the normalized standard deviation of the data matched to *bins* lines'''
    # get unit mean
    unit_mean = np.mean(y - np.min(y))
    # normalize it to be around the center
    if line is None:
        line = linear_fit(x, y, bins)
    data = line - y
    # return the normalized linear standard deviation
    return np.std(data) / unit_mean


def whisker(fig, x, y, bins=None, line_width=1, color='blue', name=None, **kwargs):
    means = []
    for bx, by in get_bins(x, y, bins):
        # find the quantiles
        vlower, low, mid, up, vupper = np.percentile(by, [10, 25, 50, 75, 90])
        xpoint = np.mean(bx)
        # plot the whisker
        fig.segment(xpoint, vlower, xpoint, vupper, line_width=line_width, line_color=color, **kwargs)
        # plot the box
        xlen = max(bx) - min(bx)
        fig.rect(xpoint, np.mean([low, up]), xlen / 10, up - low, fill_color=color, line_color=color, **kwargs)

        # plot the outliers
        outliers = np.concatenate((by[by < vlower], by[by > vupper]))
        fig.circle(np.repeat(xpoint, len(outliers)), outliers, radius=line_width, fill_color=color, line_color=color,
                   **kwargs)

        # add the mean to plot as a line later
        means.append((xpoint, mid))

    fig.line(*zip(*means), line_color=color, legend=name, **kwargs)


def scatter(fig, x, y, bins, color='blue', name=None, **kwargs):
    '''A friendly scatter plot'''
    opaque = 0.4
    drange = max(y) - min(y)
    if len(y) <= bins:
        return fig.line(x, y, color=color, legend=name,
                        line_width=2, **kwargs)
    linex, liney = mean_fit(x, y, bins)
    fig.circle(x, y, radius=drange / 1e3, fill_alpha=opaque, line_alpha=opaque,
               line_color=color, fill_color=color, legend=name, **kwargs)
    return fig.line(linex, liney, line_color=color,
                    legend=name, **kwargs)


def get_axis(fig, df):
    '''Tries to assign sets of axis to the data. Returns dictionary with column + axis to use'''
    dlen = len(df.columns)
    des = df.describe()
    total_max = np.max(des.loc['max'])
    total_min = np.min(des.loc['min'])
    fig.y_range = Range1d(start=total_min, end=total_max)
    fig.y_range.name = 'main'
    if dlen == 1:
        std = df
        small = pd.DataFrame()
    else:
        # we want to end up with two groups of data.
        total_range = total_max - total_min
        ranges = des.loc['max'] - des.loc['min']
        small = (ranges < (total_range * 0.1))
        std = des.loc[:, ~small]
        small = des.loc[:, small]
        small_max = np.max(small.loc['max'])
        small_min = np.min(small.loc['min'])

    glen = len(std.columns)
    try:
        std_colors = iter(brewer['Reds'][glen if glen > 2 else 3])
    except KeyError:
        # std_colors = tuple(zip(np.linspace(100, 255, glen + 1, dtype=int),
        #                  np.zeros(glen, dtype=int), np.zeros(glen, dtype=int)))
        std_colors = get_colors(glen, hex=True)
        std_colors = iter(std_colors)
    if not small.empty:
        fig.yaxis.axis_line_color = 'red'
        fig.extra_y_ranges = {"small": Range1d(start=small_min, end=small_max)}
        fig.add_layout(LinearAxis(y_range_name="small", axis_line_color='blue'), 'right')
        small_colors = iter(brewer['Blues'][glen if glen > 2 else 3])
    return {key: {'axis': 'small', 'color': next(small_colors)} if key in small
            else {'axis': 'main', 'color': next(std_colors)} if key in std
                  else None for key in df.columns}


def dataframe(fig, df,
              variability_cutoff: "data with variabilty > this will be box-whisker plot"=0.15,
              min_bins: "The minimum number of bins"=10,
              bins: "the desired number of bins"=30,
              num_per_bin: "dataframe will try to have at least this many data points per bin"=20,
              min_num_per_bin: "any number less than this will just be plotted as a scatter plot"=5,
              color='blue'):
    axis = get_axis(fig, df)
    for col in df.columns:
        scat = False
        data = df[col].dropna()
        if len(data) / min_bins <= num_per_bin:
            _bins = min_bins
        else:
            _bins = bins
        if len(data) / min_bins < min_num_per_bin:
            scat = True
        if not scat:
            line = linear_fit(data.index, data.values, _bins)
            std = linear_std(data.index, data.values, _bins, line=line)
            if std <= variability_cutoff:
                scat = True
        yname = axis[col]
        yname, color = yname['axis'], yname['color']
        if scat:
            if yname == 'main':
                scatter(fig, data.index, data.values, _bins, color=color, name=str(col))
            else:
                scatter(fig, data.index, data.values, _bins, color=color,
                        name=str(col), y_range_name=yname)
        else:
            if yname == 'main':
                whisker(fig, data.index, data.values, _bins, color=color,
                        name=str(col))
            else:
                whisker(fig, data.index, data.values, _bins, color=color,
                        name=str(col), y_range_name=yname)
