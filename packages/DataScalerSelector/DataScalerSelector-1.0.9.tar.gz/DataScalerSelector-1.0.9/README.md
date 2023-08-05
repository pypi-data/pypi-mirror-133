# Data Scaler Selector
![Author](https://img.shields.io/badge/author-aaneloy-blue)
[![MIT](https://img.shields.io/badge/license-MIT-5eba00.svg)](https://github.com/AmitHasanShuvo/data-inspector/blob/main/LICENCE.txt)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/AmitHasanShuvo/data-inspector)
[![Stars](https://img.shields.io/github/stars/aaneloy/data-scaler.svg?style=social)](https://github.com/aaneloy/data-scaler/stargazers)

Data Scaler Selector is an open-source python library to select the appropriate data scaler (**Min-Max, Robust or Standard Scaler**) for your Machine Learning model.


## Author: [Asif Ahmed Neloy](https://aaneloy.netlify.app/)

## Project Description:
Data Scaler is an open-source python library to select the appropriate data scaler for your Machine Learning model.


## Installation:
```
pip install DataScalerSelector
```

## Sample Notebook
In order to run the ``scalerselector_regression`` the following must be ensured:
* ``NULL`` data must be handled
* There should be no categorical variable.
* Select the ``features X`` and ``Target variable y``
* After selecting ``X`` and ``y`` run the follwing:
```
from DataScalerSelector import *

scalerselector_regression(X,y)

```

For details see this [notebook](https://github.com/aaneloy/scaler_selector/blob/main/src/notebook/Sample.ipynb)

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)