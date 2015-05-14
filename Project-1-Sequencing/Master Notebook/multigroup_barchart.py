# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt
import itertools

def bar_chart(mean_lists, std_lists, group_labels, tick_labels, colors_list=[], set_separation=.5, side_buffer=0.1):
    '''
    modified from http://matplotlib.org/examples/api/barchart_demo.html (May 10, 2015)
    
    The axis of the plot is returned so that the user may add axes labels, plot title, and legend, and make modifications.
    

    -------------------------------------------------------------------------------------

    Example:
    
    menMeans = (20, 35, 30, 35, 27)
    menStd =   (2, 3, 4, 1, 2)
    womenMeans = (25, 32, 34, 20, 25)
    womenStd =   (3, 5, 2, 3, 3)
    
    
    colors = ['r','purple']
    means = [menMeans, womenMeans]
    stds = [menStd, womenStd]
    group_labels = ('Men','Women')
    tick_labels = ('G1', 'G2', 'G3', 'G4', 'G5')
    
    ax = bar_chart(means, stds, group_labels, tick_labels, colors)
    ax.legend(loc=8)
    plt.title("Men vs. Women")
    plt.show()
    
    -------------------------------------------------------------------------------------
    future work:
    not satisfied with method of setting color scheme
    see that you can use izip longest to leave colors as an empty array
    
    and then set it later:
    
    >>>colormap = plt.cm.gist_ncar #see choosing colormaps at http://matplotlib.org/users/colormaps.html
    >>>plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, num_plots)])
    >>>for n, (means, stds, labels) in enumerate(itertools.izip_longest(means, std, group_labels)):
        ...
    '''
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%d'%int(height),
                    ha='center', va='bottom')
    
    N = max([len(i) for i in mean_lists]) #number of values in each group
    num_groups = len(mean_lists)
    
    if not colors_list:
        colormap = plt.cm.rainbow  #gist_ncar
        colors_list=[colormap(i) for i in np.linspace(0, 0.9, num_groups)]
    
    #check that lists are the same length
    lists = [std_lists, group_labels, colors_list]
    for list in lists:
        if len(mean_lists) != len(list):
            raise Exception('mean_list, std_lists, group_labels and colors_list must all be of the same length. they are {} long respectively.'.format(map(len, lists)))
    
    
    width=1.0/(num_groups+set_separation)
    ind = np.arange(N)+set_separation  # the x locations for the groups. note each value is the left most edge of a bar.
    fig, ax = plt.subplots()
    bar_groups = [] #collect for legend and labeling purposes
    
    x_max = -np.inf
    x_min = np.inf
    for n, (means, stds, labels, color) in enumerate(itertools.izip(mean_lists, std_lists, group_labels, colors_list)):
        left = ind+(n*width)
        bar_set = ax.bar(left, means, width, color=color, yerr=stds, label=labels) #add bar graphs
        autolabel(bar_set)
        bar_groups.append(bar_set)
        if x_max < left[-1]:
            x_max = left[-1]
        if x_min > left[0]:
            x_min = left[0]

    ax.set_xlim(left=x_min-side_buffer, right=x_max+width+side_buffer)

    tick_positions = ind + (width*num_groups/2)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels( tick_labels )

    return plt.gca()

if __name__ == '__main__':
    # fake data
    menMeans = (20, 35, 30, 35, 27)
    menStd =   (2, 3, 4, 1, 2)
    
    womenMeans = (25, 32, 34, 20, 25)
    womenStd =   (3, 5, 2, 3, 3)

    intersexMeans = (23,22,22,15,31)
    intersexStd = (0,0,0,0,0)#(1,4,1,5,2)
    
    # group data + setup
    colors = ['r','purple','g']
    means = [menMeans, womenMeans, intersexMeans]
    stds = [menStd, womenStd, intersexStd]

    # 3 group bar chart
    ax = bar_chart(means,stds,('Men','Women','Intersex'),('G1', 'G2', 'G3', 'G4', 'G5'))#, colors)
    ax.legend(loc=8)
    plt.show()
    
    
    # 2 group bar chart
    ax = bar_chart(means[:2],stds[:2],('Men','Women'),('G1', 'G2', 'G3', 'G4', 'G5'), colors[:2])
    ax.legend(loc=8)
    plt.show()

    
    #### other way
    means = zip(menMeans,womenMeans)
    stds = zip(menStd,womenStd)
    colors = ['r','b','g','m','c']
    ax = bar_chart(means,stds,('G1', 'G2', 'G3', 'G4', 'G5'),('Men','Women'),colors)
    ax.legend(loc=8)
    
    means = zip(menMeans,womenMeans,intersexMeans)
    stds = zip(menStd,womenStd,intersexStd)
    colors = ['r','b','g','m','c']
    ax = bar_chart(means,stds,('G1', 'G2', 'G3', 'G4', 'G5'),('Men','Women','Intersex'),colors)
    ax.legend(loc=8)
    
    plt.show()
