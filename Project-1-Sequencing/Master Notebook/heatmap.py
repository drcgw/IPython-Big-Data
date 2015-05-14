'''
Note to self:
For example of how to handle the annotation_function issue see
http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.apply.html#pandas.DataFrame.apply
'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
import os, sys, re

def show_values(pc, fmt="%.2f", **kw):
    '''
    Handy little function to print the array used to create a heatmap into the squares of the map.
    
    CREDIT:
    code posted by: pelson
    to stackoverflow @ http://stackoverflow.com/questions/11917547/how-to-annotate-heatmap-with-text-in-matplotlib
    accessed on May 1 2015 (at this time the most recent edit had occured at Aug 11 '12 at 22:18)
    
    ARGS:
        pc: the matplotlib.pyplot.pcolor instance
        fmt: a string containing formating instructions for the values
        kw: dict of key-word args for ax.text
    RETURNS:
        None
    '''
    
    from itertools import izip
    pc.update_scalarmappable()
    ax = pc.get_axes()
    #print pc.get_array()
    for p, color, value in izip(pc.get_paths(), pc.get_facecolors(), pc.get_array()):
        x, y = p.vertices[:-2, :].mean(0)
        if np.all(color[:3] > 0.5):
            color = (0.0, 0.0, 0.0)
        else:
            color = (1.0, 1.0, 1.0)
        ax.text(x, y, fmt % value, ha="center", va="center", color=color, **kw)


def heatmap_from_array(data, ax = None, colors = plt.cm.Blues, x_labels=[], y_labels=[], colorbar_label='', annotate_function=show_values, vmin_vmax=None):
    '''
    The annotate function should have defaults for all args but the pcolorplot arg set to desired values. (how should I change this to make it better?)
    To remove annotation pass annotate_function=lambda pcolorplot,fmt='': ''
    
    '''
    if not ax:
        ax = plt.gca()
    
    
    if vmin_vmax:
        v_min,v_max = vmin_vmax
        cax = ax.pcolor(data, cmap=colors, vmin=v_min, vmax=v_max)
        cbar_tick_label = np.linspace(v_min,v_max,10)#int(dmin),int(dmax))#[dmin, dmin+(dmax-dmin)/2, dmax]

    else:
        #determine min and max for data
        dmin, dmax = round(data.min(),2),round(data.max(),2)#np.floor(data.min()), np.ceil(data.max())
        cax = ax.pcolor(data, cmap=colors, vmin=dmin, vmax=dmax)
        cbar_tick_label = np.linspace(dmin,dmax,10)#int(dmin),int(dmax))#[dmin, dmin+(dmax-dmin)/2, dmax]

    annotate_function(cax)
    '''
    try:
        annotate_function(cax)
    except:
        print """The annotate function should have defaults for all args but the pcolorplot arg set to desired values."""
    '''
    # put the major ticks at the middle of each cell
    w = 0.5
    ax.set_xticks(np.arange(data.shape[1])+w, minor=False)
    ax.set_yticks(np.arange(data.shape[0])+w, minor=False)
    ax.set_xticklabels(x_labels, minor=False)
    ax.set_yticklabels(y_labels, minor=False)

    #set colorbar labels based on plot min and max values
    cbar = plt.colorbar(cax, ticks=cbar_tick_label)
    cbar.set_label(colorbar_label)
    cbar.set_ticklabels([round(i,2) for i in cbar_tick_label])

    return plt.gca(), cbar


def heatmap_from_dataframe(dataframe, ax=None, colors = plt.cm.Blues, colorbar_label = '', annotate_function = show_values, vmin_vmax = None):
    '''
    To remove annotation pass annotate_function=lambda pcolorplot,fmt='': ''

    '''
    
    label1, label2 = dataframe.columns.values, dataframe.index.values
    data = np.array(dataframe.values)
    
    return heatmap_from_array(data, ax, colors, label1, label2, colorbar_label,  annotate_function, vmin_vmax)



if __name__ == '__main__':
    def main():
        #main function

        measure = 'Intraburst Interval'
        
        test_data = [[ 3.38444863,  3.34091236,  2.71575965],
         [ 3.33215736,  3.08020728,  1.87674438],
         [ 3.27351859,  2.45086207,  1.38714046],
         [ 3.06368102,  1.94385315,  1.04590535],
         [ 2.75519466,  1.63226804,  0.82575777]]
         
        test_index = [1.8, 2.4, 3.0, 3.6, 4.2]
        test_columns = [u'-65.0', u'-60.0', u'-55.0']
        
        fig0 = plt.figure(0)
        ax1 = fig0.add_subplot()
        
        ax1, colorbar1 = heatmap_from_array(np.array(test_data), ax1, x_labels = test_columns, y_labels = test_index, colorbar_label = measure+' (s)', annotate_function = show_values, vmin_vmax=(0,4.))

        ax1.set_title(measure)
        ax1.set_xlabel(r'eL (mV)')
        ax1.set_ylabel(r'$g_{nap}$ (nS)')

        fig1 = plt.figure(1)
        ax2 = fig1.add_subplot()

        df = pd.DataFrame(data = test_data, index = test_index, columns = test_columns)
        ax2, colorbar2 = heatmap_from_dataframe(df, ax=ax2, colorbar_label = measure+' (s)', annotate_function = show_values)
        
        plt.show()

    main()

