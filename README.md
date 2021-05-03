
![Image](http://troya.tv/UnderConstruction.png)

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">

# Fuel Vs. Food (Beta)  :relieved:	


Nikola tesla:

>The present is theirs; the future, for which I really worked, is mine




**Project Target:** :weight_lifting_man:

Create a smart annual predictions algorithm to predict the diverting of crops (such as :Wheat, Maize, Other coarse grains, Vegetable oils, Molasses etc...) for biofuels production, Feed and food supply.

Predictions will relay on the quantity of Export, Imports, Production, R&D budget investment and more.

Depend on API:
•	OECD.Stat database – Agricultural & Government funds datasets. :globe_with_meridians:	

•	yahoo finance API. :money_with_wings:

•	More to come...


<img
  style="width: 100%; margin: auto; display: block;"
  class="vidyard-player-embed"
  src="https://play.vidyard.com/o7T935ZzQpjSw7xEuiWfU3.jpg"
  data-uuid="o7T935ZzQpjSw7xEuiWfU3"
  data-v="4"
  data-type="inline"
/>


## check list: :bookmark_tabs:

- [x] OECD API.
- [x] yahoo finance API ().
- [ ] More data sources.
- [x] initial Sqlite Database.
- [x] initial batch file (offline start-up).
- [ ] Divide countries by continent.
- [x] local web app (Streamlit) (**beta**).
- [ ] Data preparation (NumPy).
- [ ] Gradient descent testing.
- [ ] Line regression testing.
- [ ] Decision tree testing.
- [ ] 'Slim code' rev.
- [ ] Full Logging framework.
- [ ] Full docstring.
- [ ] Updated requirement.txt file.
- [ ] Dockerized applications (optional).
- [ ] Django/Flask framework (optional).
- [ ] plotly dash with react(.js) base UI a (optional).
- [ ] Deploy.

## liberies in use:  :statue_of_liberty:	
 
```python
import sys
import os
import sqlite3 
import streamlit
import pandas 
import time
import datetime
import plotly.graph_objects 
import requests
import xmltodict
import pandasdmx
import currency_converter
import logging
import pathlib 
```


## liberies in use:

useful datasets | unuseful datasets
------------ | -------------
OECD.stat | yahoo finance


To be continued...

