""""
Single function for use in SF Python talks; also part of standard data science setup
"""

import pandas as pd

def df_crossjoin(df1, df2, **kwargs):
    """
    Function to create the cartesian product of all rows between two DataFrames without existing matching keys
    Returns a single DataFrame with mulitindex, that can be appended to a result set
    Intended for use within a loop, or with df.apply
    """
    # disable `SettingWithCopyWarning` warning, which is not an issue in this use case
    pd.options.mode.chained_assignment = None   # default='warn'

    # create temporary keys in each DataFrame
    # such that each row gets a matching key column, with each row getting a unique number as a key
    # this allows us to use pandas merge function, and create the product of all rows from the
    # left dataframe, with all rows on the right dataframe
    df1['_tmpkey'] = 1
    df2['_tmpkey'] = 1

    result_join = pd.merge(df1, df2, on='_tmpkey', **kwargs).drop('_tmpkey', axis=1)
    result_join.index = pd.MultiIndex.from_product((df1.index, df2.index))

    df1.drop('_tmpkey', axis=1, inplace=True)
    df2.drop('_tmpkey', axis=1, inplace=True)

    return result_join
