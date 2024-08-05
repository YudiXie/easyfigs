import numpy as np
from matplotlib import pyplot as plt


def remove_top_right_spines(ax=None):
    if ax is None:
        ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def add_errorbars(ax, data_dict, **kwargs):
    """
    Args:
        data_dict: dict, the data to plot,
            each key is the group label of a set of points
            each value is a dict with keys 'x', 'y', 'error'
            they are list or array of the same length
            'x' is the x axis data
            'y' is the y axis data
            'error', optional, is the error bar data
            'color', optional, is the color of the points
        kwargs: dict, additional keyword arguments for errorbar
            will overwrite the default values
    """
    for key, value in data_dict.items():
        ebar_kwargs = {'fmt': "o-", 'capsize': 3}
        ebar_kwargs.update(kwargs)
        if 'error' in value:
            ebar_kwargs.update({'yerr': value['error']})
        if 'color' in value:
            ebar_kwargs.update({'color': value['color']})
        ax.errorbar(value['x'], value['y'], label=key, **ebar_kwargs)


def add_filled_lines(ax, data_dict, **kwargs):
    """
    Args:
        data_dict: dict, the data to plot,
            each key is the group label of a set of points
            each value is a dict with keys 'x', 'y', 'error'
            they are list or array of the same length
            'x' is the x axis data
            'y' is the y axis data
            'error', optional, is the error bar data, this overwrites the lower or upper
            'lower', 'upper', optional, is the error bar data
            'color', optional, is the color of the points
    """
    for key, value in data_dict.items():
        fl_kwargs = {}
        if 'color' in value:
            fl_kwargs.update({'color': value['color']})
        kwargs.update(fl_kwargs)
        ax.plot(value['x'], value['y'], label=key, **kwargs)
        if 'error' in value:
            value['lower'] = np.array(value['y']) - np.array(value['error'])
            value['upper'] = np.array(value['y']) + np.array(value['error'])
        if ('lower' in value) and ('upper' in value):
            ax.fill_between(value['x'], value['lower'], value['upper'],
                            alpha=0.2, linewidth=0.0, **fl_kwargs)


def bar_groups(ax,
               x_axis_labels,
               data_dict,
               ylim=None,
               x_label=None,
               y_label=None,
               fig_title=None,
               bar_label=True,
               legend_title=None,
               legend_fontsize=10,
               ):
    """
    make a bar plot of multiple groups of data

    Args:
        data_dict: dict, the data to plot,
            each key is the group label of a set of points
            each value is a dict with keys 'x', 'y', 'error'
            they are list or array of the same length
            'x' is the x axis data (optional)
            'y' is the y axis data (same length as x_axis_labels)
            'error', optional, is the error bar data
            'color', optional, is the color of the points
    """
    num_groups = len(data_dict.keys())
    width = 0.7 / num_groups  # the width of the bars
    x_axis = np.arange(len(x_axis_labels))  # the label locations

    for (i, (key, value)) in enumerate(data_dict.items()):
        assert len(value['y']) == len(x_axis_labels)
        offset = i * width - ((num_groups - 1) * width / 2)
        kwargs = {'label': key, 'capsize': width*15, 'ecolor': 'black', 'alpha': 0.5}
        if 'error' in value:
            kwargs['yerr'] = value['error']
        if 'color' in value:
            kwargs['color'] = value['color']
        rect = ax.bar(x_axis + offset, value['y'], width, **kwargs)
        if bar_label:
            ax.bar_label(rect, padding=3, fmt='%.2f')

    ax.set_xticks(x_axis, x_axis_labels)

    legend_kwargs = {'title': legend_title, 'fontsize': legend_fontsize}
    ax.legend(**legend_kwargs)

    axis_kwargs = {'ylim': ylim,
                   'xlabel': x_label,
                   'ylabel': y_label,
                   'title': fig_title,
                   }
    ax.set(**axis_kwargs)
    remove_top_right_spines(ax)
    return rect
