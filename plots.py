from csv_tools import read_from_csv, fields_select, rows_to_2dcoordinates, field_apply, get_mapping, csv_sort, get_prior_map
from plot_tools import n_plot_bar

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='plot')
    parser.add_argument('--plot-type', default='normal', choices=['normal', 'increasement'])
    parser.add_argument('--data-path', default='results/walker.csv', type=str, help='The path to the data')
    parser.add_argument('--save-path', default='results/walker.pdf', type=str, help='The path to save the plot')
    parser.add_argument('--n-axis', default='model_name', type=str, help='The field name of n subplots')
    parser.add_argument('--x-axis', default='adv_type', type=str, help='The field name of x axis')
    parser.add_argument('--y-axis', default='mAP_50', type=str, help='The field name of y axis')

    args = parser.parse_args()
    
    data = read_from_csv(args.data_path)
    new_fileds = 'model_name', 'adv_type', 'mAP_50'
    data = fields_select(data, fields=new_fileds)

    # sort the data based on the adversarial type and list the 'clean' and 'random' first
    data = csv_sort(data, 'adv_type', get_prior_map(['clean', 'random']))

    # convert the mAP_50 to float
    data = field_apply(data, 'mAP_50', float)

    # mapping the model name to the short name
    mapping_csv = read_from_csv('results/mapping_model_name.csv')
    data = field_apply(data, 'model_name', get_mapping(mapping_csv))


    # mapping the adversarial type to the short name
    mapping_csv = read_from_csv('results/mapping_adv_type.csv')
    data = field_apply(data, 'adv_type', get_mapping(mapping_csv))

    fields, rows = data

    # convert the rows to 2d coordinates
    n, x, y = rows_to_2dcoordinates(rows)

    
    # plot the bar plot for each model and concatenate the plots
    plot = n_plot_bar('model', 'adversarial type', 'mAP 50', n, x, y, ticks=[0,0.2,0.4,0.6,0.8,1], columns=8, direction='horizontal')

    # save the plot to pdf
    plot.savefig(args.save_path, dpi=300)
    