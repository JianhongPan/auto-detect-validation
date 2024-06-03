from turtle import width
import numpy as np
import matplotlib.pyplot as plt
from csv_tools import read_from_csv, fields_select, rows_to_2dcoordinates


def n_plot_bar(title, x_label, y_label, n, x, y, columns, direction='vertical', legend=False):
    '''
    Plot n bar plots for each model and concatenate the plots
    '''
    n = n[:-(len(n) % columns)]
    n = np.array(n).reshape(-1, columns)
    if direction == 'vertical':
        fig, axss = plt.subplots(n.shape[0], n.shape[1], figsize=(9, 8))
    else:
        fig, axss = plt.subplots(n.shape[0], n.shape[1], figsize=(10, 10))

    # from warm to cold len(x) colors
    if len(x) > 20:
        raise ValueError("The color sapce can not satisfy the legend")
    color_scaler = np.linspace(0, 1, len(x)).tolist()
    colors = plt.cm.tab20b(color_scaler)

    for i, axs in enumerate(axss):
        for j, ax in enumerate(axs):
            if direction == 'vertical' and j == 0:
                ax.set_ylabel(y_label)
            if direction == 'horizontal' and i == len(axss) - 1:
                ax.set_xlabel(y_label)

            ax.set_title(n[i, j])

            # set the frame width of the plot
            for spine in ax.spines.values():
                spine.set_linewidth(0.5)

            # remove the y label for the plots except the first column
            if j != 0:
                if direction == 'vertical':
                    ax.set_xticklabels([])
                    ax.set_xticks([])
                else:
                    ax.set_yticklabels([])
                    ax.set_yticks([])

            # set the tick direction and width
            ax.tick_params(direction='in')
            ax.tick_params(width=0.5)

            if direction == 'vertical':
                # set the vertical grid at the backgroud
                ax.yaxis.grid(True)
                ax.yaxis.grid(linewidth=0.1)
                ax.set_axisbelow(True)
                ax.set_yticks(np.arange(0, 1.1, 0.2))
            else:
                # set the vertical grid at the backgroud
                ax.xaxis.grid(True)
                ax.xaxis.grid(linewidth=0.1)
                ax.set_axisbelow(True)
                ax.set_xticks(np.arange(0, 1.1, 0.2))
                # set the tick width

            # plot the bar plot for each model with different adversarial type as different color
            for k, x_k in enumerate(x):
                if direction == 'vertical':
                    ax.bar(x_k, y[i * columns + j][k], color=colors[k], label=x_k, width=0.5, edgecolor='black', linewidth=0.5)
                else:
                    ax.barh(x_k, y[i * columns + j][k], color=colors[k], label=x_k, height=0.6, edgecolor='black', linewidth=0.5)
            
            if direction == 'vertical':
                # set the vertical grid at the backgroud
                ax.yaxis.grid(True)
                ax.yaxis.grid(linewidth=0.1)
                ax.set_axisbelow(True)
                ax.set_yticks(np.arange(0, 1.1, 0.2))
            else:
                # set the vertical grid at the backgroud
                ax.xaxis.grid(True)
                ax.xaxis.grid(linewidth=0.1)
                ax.set_axisbelow(True)
                ax.set_xticks(np.arange(0, 1.1, 0.2))
                # set the tick width

    for i, axs in enumerate(axss):
        for j, ax in enumerate(axs):
            for k, rect in enumerate(ax.patches):
                # set the bar in the middle of the x ticks
                if direction == 'vertical':
                    rect.set_x(rect.get_x() + 0.2)
            

    # set the all the font to Times New Roman
    font = 'Times New Roman'
    for ax in axss.flatten():
        ax.set_title(ax.get_title(), fontname=font, fontsize=8, fontweight='bold')
        ax.set_ylabel(ax.get_ylabel(), fontname=font, fontsize=6)
        ax.set_xlabel(ax.get_xlabel(), fontname=font, fontsize=6)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontname(font)
            label.set_fontsize(6)

    # set the margin of the plot
    plt.tight_layout()

    # setting the interval between the plots
    plt.subplots_adjust(wspace=0.2, hspace=0.4)

    if legend:    
        # set the legend for each adv type
        legend = fig.legend(x, loc='lower center', fontsize=10, title=x_label, ncol=len(x)//2)
        legend.get_frame().set_edgecolor('black')
        plt.subplots_adjust(bottom=0.15)
        plt.setp(legend.get_title(), fontname=font)
        plt.setp(legend.get_texts(), fontname=font)

    
    return fig
