# pandaSuit <img align="right" alt="Panda in a Suit" height="138" width="96" src="https://github.com/AnthonyRaimondo/pandaSuit/raw/main/static/logo/pandaSuit-mini.ico?raw=true" title="Panda in a Suit" />
Extension of the [pandas](https://github.com/pandas-dev/pandas#what-is-it) library to encapsulate some of the most used methods of querying and manipulating DataFrames. Also featuring reversible DataFrame operations, creation of plot and dashboard objects, and methods for producing regression models.

The pandaSuit.DF class inherits from pandas.DataFrame, so a pandaSuit DF object can be treated as a pandas DataFrame. The additional features merely augment the core pandas DataFrame, or dress it up. Hence, a _panda in a suit_.


## How to install - [PyPI](https://pypi.org/project/pandaSuit/)
```pip install pandaSuit```


## Dependencies
* [pandas](https://github.com/pandas-dev/pandas#where-to-get-it) >=1.3.4
* [scikit-learn](https://github.com/scikit-learn/scikit-learn#user-installation) >=1.0.1
* [matplotlib](https://github.com/matplotlib/matplotlib#install) >=3.5.1

____________________________________________________________________________________________________
## Examples
### _Querying_
__Query DF object by column name__ <img alt="select-by-column-name" width="700" src="https://github.com/AnthonyRaimondo/pandaSuit/raw/main/static/examples/select-by-column-name.PNG?raw=true" title="select-by-column-name" />
____________________________________________________________________________________________________
__Or by index, possibly for rows and columns__ <img alt="select-by-index" width="700" src="https://github.com/AnthonyRaimondo/pandaSuit/raw/main/static/examples/select-by-index.PNG?raw=true" title="select-by-index" />
____________________________________________________________________________________________________
__Equivalent to existing pandas functionality__ <img alt="use-core-pandas-methods" width="700" src="https://github.com/AnthonyRaimondo/pandaSuit/raw/main/static/examples/use-core-pandas-methods.PNG?raw=true" title="use-core-pandas-methods" />
____________________________________________________________________________________________________
#
### _Manipulation_
__Update values at specific locations__ <img alt="update-specific-location" width="700" src="https://github.com/AnthonyRaimondo/pandaSuit/raw/main/static/examples/update-specific-location.PNG?raw=true" title="update-specific-location" />
____________________________________________________________________________________________________
__Undo changes made to DF object__ <img alt="undo-DF-manipulation" width="700" src="https://github.com/AnthonyRaimondo/pandaSuit/raw/main/static/examples/undo-DF-manipulation.PNG?raw=true" title="undo-DF-manipulation" />
____________________________________________________________________________________________________
#
### _Visualization_
__Create plots from DF objects__ <img alt="create-a-plot" width="700" src="https://github.com/AnthonyRaimondo/pandaSuit/raw/main/static/examples/create-a-plot.PNG?raw=true" title="create-a-plot" />
____________________________________________________________________________________________________
__Make dashboards with multiple plots__ <img alt="create-a-dashboard" width="700" src="https://github.com/AnthonyRaimondo/pandaSuit/raw/main/static/examples/create-a-dashboard.PNG?raw=true" title="create-a-dashboard" />
____________________________________________________________________________________________________
__Add new plots to a dashboard__ <img alt="add-to-dashboard" width="700" src="https://github.com/AnthonyRaimondo/pandaSuit/raw/main/static/examples/add-to-dashboard.PNG?raw=true" title="add-to-dashboard" />
____________________________________________________________________________________________________