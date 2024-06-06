from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import random

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='plot')
    parser.add_argument('--benchmark', type=str, choices=['weather', 'distance', 'rotation-theta', 'rotation-phi', 'sphere', 'spot', 'entire'], default='entire', help='Name of the benchmark')
    parser.add_argument('--data-path', default='results/vehicle.csv', type=str, help='The path to the data')
    parser.add_argument('--save-path', default='results/vehicle.pdf', type=str, help='The path to save the plot')
    parser.add_argument('--n-axis', default='model_name', type=str, help='The field name of n subplots')
    parser.add_argument('--x-axis', default='adv_type', type=str, help='The field name of x axis')
    parser.add_argument('--y-axis', default='mAR 50', type=str, help='The field name of y axis')

    args = parser.parse_args()
    
    # read the data of given fields from the csv file
    data = pd.read_csv(args.data_path, usecols=['benchmark', args.n_axis, args.x_axis, args.y_axis])

    # filter the data based on the benchmark
    data = data[data['benchmark'] == args.benchmark]

    # sort the data based on the adversarial type
    data = data.sort_values(by=[args.x_axis], ascending=True)

    # changing the model name to the short name
    mapping_csv = pd.read_csv(f'results/mapping_{args.n_axis}.csv')
    data[args.n_axis] = data[args.n_axis].map(dict(zip(mapping_csv['from'], mapping_csv['to'])))

    # mapping the adversarial type to the short name
    mapping_csv = pd.read_csv(f'results/mapping_{args.x_axis}.csv')
    data[args.x_axis] = data[args.x_axis].map(dict(zip(mapping_csv['from'], mapping_csv['to'])))

    # pivot the data to 3D coordinates
    data = data.pivot(columns=args.n_axis, index=args.x_axis, values=args.y_axis)

    # list 'Clean' and 'Random' first in the adversarial type
    data_clean = data.reindex(['Clean', 'Random'], axis=0) 
    data_non_clean = data.drop(['Clean', 'Random'], axis=0)
    data = pd.concat([data_clean, data_non_clean])

    # plot the data
    columns = 12
    rows = int(np.ceil(data.shape[1] / columns))
    axss = data.plot(kind='barh', layout=(rows, columns), figsize=(12, 7), subplots=True, legend=False, width=1)
    cm = plt.get_cmap(random.choice(['tab20', 'tab20b', 'tab20c']))
    font = 'Times New Roman'


    # set the title for each subplot
    for i, axs in enumerate(axss):
        for j, ax in enumerate(axs):

            # set the frame width of each subplot
            for spine in ax.spines.values():
                spine.set_linewidth(0.5)
            # remove the y label for the subplots except the ones in the first column
            if j != 0:
                ax.set_ylabel('')
                ax.set_yticks([])
            else:
                ax.set_ylabel('Attack Method')

            # set the tick direction and width
            ax.xaxis.set_tick_params(which='both', labelbottom=True)
            # set the x label and x ticks
            ax.set_xlabel(f'{args.y_axis}(%) / ASR(%)')
            ax.tick_params(direction='in')
            ax.tick_params(width=0.5)
            # set the x grid at the backgroud
            ax.xaxis.grid(True)
            ax.xaxis.grid(linewidth=0.1)
            ax.set_axisbelow(True)
            ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
            ax.set_xticklabels(['0', '20', '40', '60', '80', '100'])
            ax.set_xlim([0, 1.0])

            # set the bar plot for each model with different adversarial type as different color
            for k, bar in enumerate(ax.patches):
                bar.set_height(0.6)
                bar.set_y(bar.get_y() + 0.3)
                bar.set_color(cm(k % 20))
                bar.set_edgecolor('black')
                bar.set_linewidth(0.5)
                bar.set_alpha(0.3)


            # scatter plot for the percentage of the adversarial type to the clean data
            if ax.get_title() != '':
                # set scatter plot for each adversarial type to show the percentage to the clean data
                bars_value = data.loc[:][ax.get_title()]
                bars_asr = 1 - bars_value/bars_value.loc['Clean']                
                ax.scatter(bars_asr, range(len(bars_asr)), s=30, c='black', marker='P')
            # set color of the scatter plot
            for k, scatter in enumerate(ax.collections):
                scatter.set_color(cm(k % 20))
                scatter.set_edgecolor('white')
                scatter.set_linewidth(0.5)
                scatter.set_offsets(np.c_[scatter.get_offsets()[:, 0], scatter.get_offsets()[:, 1] + 0.1])

    
            # set the all the font to Times New Roman
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

    # save the plot to pdf
    plt.savefig(args.save_path, dpi=300)
    