from copy import copy
import pandas as pd
import numpy as np
import re
from sklearn.cluster import KMeans
from plotnine import ggplot, aes, geom_histogram, geom_point, geom_line, geom_col, labs, theme, element_text
from my_python_extensions.msand import theme_msand

def plot_numeric_variable_distribution(data, column, log10 = False, **kwargs):
    """
    Plots the histogram of one column from a Pandas DataFrame.
    
    Args:
        data ([Pandas DataFrame]): 
            A pandas data frame with the column you want to visualize. 
        column ([str]): 
            The string name of a single numeric column. Must be int64 or float64.
        log10 (bool, optional): 
            Transforms the column's data by using np.log10. Defaults to False.
        kwargs: Passed to geom_histogram()
        
    Returns:
        ggplot object: A histogram plot.
    """
    # CHECKS

    if (type(data) is not pd.DataFrame):
        raise TypeError("`data` is not Pandas Data Frame.")

    if type(column) is not str:
        raise TypeError("`column` name is not string.")
    
    if data.dtypes[column] not in [np.int64, np.float64]:
        raise TypeError("`column` dtype is not int64 or float64.")
    
    if type(log10) is not bool:
        raise TypeError("`log10` is not logical.")
        
    # BODY
     
    data = copy(data)
    
    readable_column = re.sub(r'(\w)([A-Z])', r'\1 \2', column)
    
    if log10:
        data[column] = np.log10(data[column])
        readable_column = readable_column + ' Log10'
    
    g = ggplot(aes(x = column), data=data) + \
        geom_histogram(**kwargs) + \
        theme_msand() + \
        labs(
            title = 'Distribution of ' + readable_column,
            x = readable_column,
            y = 'Count'
        )
        
        
    return g


def kmeans_inertia_plot(features, max_clusters, plot_title):
    """
    Plots the ineria from 1 to a specified number of max clusters.

    Args:
        features (ndarray): The data you want to cluster
        max_clusters (int): The max number of clusters 
        plot_title (str): A string containg the title of the plot

    Returns:
        ggplot object: A plot with the number of clusters on the x-axis and inertia value on the y-axis.
    """
    
    ks = range(1, max_clusters)
    inertias = []
    for k in ks:
        # Create a KMeans instance with k clusters: model
        model = KMeans(n_clusters = k)
        
        # Fit model to samples
        model.fit(features)
        
        # Append the inertia to the list of inertias
        inertias.append(model.inertia_)
    
    g = ggplot(aes(ks, inertias)) + \
        geom_point(size = 4, color = '#F1C761') + \
        geom_line(size = 1, color = '#F1C761') + \
        theme_msand() + \
        labs(
            title = plot_title,
            x = 'Number of Clusters (k)',
            y = 'Inertia'
        )
        
    return g
        
def customer_column_count_visualization(data, column, column_value):
    """
        Plots the frequency of a categorical column value by customer.

    Args:
        data ([Pandas DataFrame]): 
            A pandas data frame with the column you want to visualize. 
        column ([str]): 
            The string name of a single categorical column. 
        column_value ([str]): 
            The category within the categorical column you want to visualize.

    Returns:
        ggplot object: 
            A plot with the customer id on the x-axis and the frequency of the column value on the y-axis.
    """

    my_order = data \
        .sort_values('CustomerId') \
        .CustomerId \
        .unique() \
        .tolist()

    gdata = data[data[column] == column_value] \
        .drop(list(data.filter(regex='Clusters$')), axis=1) \
        .groupby('CustomerId') \
        .count() \
        .reindex(data.CustomerId.unique(), fill_value = 0) \
        .reset_index(drop = False) \
        .sort_values('CustomerId') \
        .reset_index(drop = True) \
        .assign(CustomerId = lambda x: pd.Categorical(x['CustomerId'], categories=my_order))

    g = ggplot(aes(gdata.CustomerId, gdata[column])) + \
        geom_col(fill = '#F1C761', color = '#333333') + \
        theme_msand() + \
        theme(figure_size=(12, 8),
            axis_text_x=element_text(rotation=90)) + \
        labs(
            title = 'Frequency of ' + column_value + ' Across Customers',
            x = 'Customer Id',
            y = 'Count'
        )
        
    return g