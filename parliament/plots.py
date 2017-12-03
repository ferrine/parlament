import matplotlib.pyplot as plt


def pie_stat(hor, stat, ax=None, fig_kwargs=None, **pie_kwargs):
    dict_stat = hor.map_stat(stat)
    stat_name = stat if isinstance(stat, str) else stat.__name__
    if ax is None:
        if fig_kwargs is None:
            fig_kwargs = {}
        _, ax = plt.subplots(**fig_kwargs)
    ax.set_title('{} of {}'.format(stat_name, hor.name))
    ax.pie(list(dict_stat.values()), labels=dict_stat.keys(), **pie_kwargs)
    ax.axis('equal')
    return ax
