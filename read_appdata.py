import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def paid_app(dataset):
    """
    Plot a rating vs. price scatter plot of paid applications.

    Args:
        dataset: A dataframe that contains the application informations.
    """
    # Filter out the data that are free.
    not_free = dataset[(dataset['price'] > 0.0)]

    # Plot a scatter plot of rating vs. price only with applications
    # that are not free.
    plt.plot(not_free['price'], not_free['score'], 'go')

    # Limit the axis since that there aren't many applications that are
    # more expensive than 40 dollars and they make the graph difficult
    # to observe.
    plt.axis([0, 40, -0.1, 5.1])

    plt.xlabel('Price ($)')
    plt.ylabel('Ratings out of 5')
    plt.title('Rating vs Price for Paid Applications')


def box_plot_genre(dataset):
    """
    Plot a rating vs. genre box plot of applications.

    Args:
        dataset: A dataframe that contains the application informations.
    """
    # Group the data with genre and count the number of applications
    # in each genre.
    grouped_genre = dataset['genre'].value_counts()

    # Filter the data of genre that count is over 100 so that it
    # eliminates the genre with insufficient number of data.
    filtered_genre = grouped_genre[grouped_genre > 20]

    # Get the name of the filtered genre into list.
    genre_list = filtered_genre.index.tolist()

    # Filter the application data that their genre are in the
    # filtered list.
    boxdata = dataset['genre'].isin(genre_list)
    filtered_df = dataset[boxdata]

    box = sns.boxplot(x='genre', y='score', data=filtered_df)

    box.set(title='Rating vs. Genre of the Google Play Applications',
            xlabel='Genre', ylabel='Ratings out of 5')

    # Rotate the x axis label to make it easier to read.
    box.set_xticklabels(box.get_xticklabels(), rotation=90)


def cat_plot_content(dataset):
    """
    Plot a rating vs. content categorical plot of applications.

    Args:
        dataset: A dataframe that contains the application informations.
    """
    # Create a categorical plot of rating vs. content rating.
    cat = sns.catplot(x='contentRating', y='score', data=dataset)
    cat.set(title='Rating vs Content Rating of Applications',
            xlabel='Content Ratings', ylabel='Ratings out of 5')

    # Rotate the x axis label to make it easier to read.
    cat.set_xticklabels(rotation=90)


def neat_data(dataset):
    """
    Return a dataframe that rename the 'size' column, remove rows
    that size is not defined, and change the values into float.

    Args:
        dataset: A dataframe that contains the application informations.

    Returns:
        A dataframe that has cleaner data of size column.
    """

    # Filter the dataset that the value in size column ends with 'M'
    # so that it removes the rows that size is not defined.
    filtered = dataset['size'].str.endswith('M')
    sized_dataset = dataset[filtered]

    # Rename the 'size' column to differentiate from the function
    # with same name, and make the 'size' values into list.
    renamed_data = sized_dataset.rename(columns={'size': 'appSize'})
    size_list = renamed_data.appSize.tolist()

    # Set an empy list to hold the new size values that are float.
    new_size_list = []

    for sizes in size_list:
        new_size_list.append(float(sizes.split('M', 1)[0]))

    neat_df = renamed_data.assign(appSize=new_size_list)
    return neat_df


def size_and_rating(dataset):
    """
    Plot a rating vs. size linear regression plot of applications.

    Args:
        dataset: A dataframe that contains the application informations.
    """
    # Filter the dataframe of applications with app size smaller than
    # 300M to remove the outliers.
    filtered_data = dataset[(dataset['appSize'] < 300)]

    # Group the appsize column into size of 3M and remove the NaN values.
    ranged_data = filtered_data.groupby(pd.cut(filtered_data['appSize'],
                                        np.arange(0, 300, 3))).mean().dropna()

    sizeplot = sns.lmplot(data=ranged_data, x='appSize', y='score')
    sizeplot.set(title='Ratings vs. Size of Applications', xlabel='Size',
                 ylabel='Ratings out of 5')


def free_and_paid(dataset):
    """
    Plot a rating vs. free/paid categorical plot of applications.

    Args:
        dataset: A dataframe that contains the application informations.
    """
    # Create a categorical plot of rating over free and paid applications.
    cat = sns.catplot(x='free', y='score', data=dataset)
    cat.set(title='Ratings over Free and Paid Applications',
            xlabel='Free', ylabel='Ratings out of 5')
