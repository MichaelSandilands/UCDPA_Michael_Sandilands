# Specialist Certificate in Data Analytics Essentials Assignment

## Chapter 4: Data Preparation and Feature Engineering

## Imports


```python
%cd ..
```

    /home/michael/Documents/python_projects/UCDPA_Michael_Sandilands



```python
import pandas as pd
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from umap import UMAP
```

## Import Data


```python
invoice_lines_df = pd.read_csv('./00_Data/invoice_lines.csv')

invoice_lines_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>InvoiceLineId</th>
      <th>InvoiceId</th>
      <th>CustomerId</th>
      <th>UnitPrice</th>
      <th>Quantity</th>
      <th>TrackName</th>
      <th>Composer</th>
      <th>Milliseconds</th>
      <th>Bytes</th>
      <th>GenreName</th>
      <th>AlbumTitle</th>
      <th>ArtistName</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>0.99</td>
      <td>1</td>
      <td>Balls to the Wall</td>
      <td>NaN</td>
      <td>342562</td>
      <td>5510424</td>
      <td>Rock</td>
      <td>Balls to the Wall</td>
      <td>Accept</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>2</td>
      <td>0.99</td>
      <td>1</td>
      <td>Restless and Wild</td>
      <td>F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. D...</td>
      <td>252051</td>
      <td>4331779</td>
      <td>Rock</td>
      <td>Restless and Wild</td>
      <td>Accept</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>2</td>
      <td>4</td>
      <td>0.99</td>
      <td>1</td>
      <td>Put The Finger On You</td>
      <td>Angus Young, Malcolm Young, Brian Johnson</td>
      <td>205662</td>
      <td>6713451</td>
      <td>Rock</td>
      <td>For Those About To Rock We Salute You</td>
      <td>AC/DC</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>2</td>
      <td>4</td>
      <td>0.99</td>
      <td>1</td>
      <td>Inject The Venom</td>
      <td>Angus Young, Malcolm Young, Brian Johnson</td>
      <td>210834</td>
      <td>6852860</td>
      <td>Rock</td>
      <td>For Those About To Rock We Salute You</td>
      <td>AC/DC</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>2</td>
      <td>4</td>
      <td>0.99</td>
      <td>1</td>
      <td>Evil Walks</td>
      <td>Angus Young, Malcolm Young, Brian Johnson</td>
      <td>263497</td>
      <td>8611245</td>
      <td>Rock</td>
      <td>For Those About To Rock We Salute You</td>
      <td>AC/DC</td>
    </tr>
  </tbody>
</table>
</div>



## Gathering Features

I plan to cluster each of our variables, 'GenreName', 'ArtistName' and 'Milliseconds', seperately. Allowing us to make inferences about how customers are segmented across each different variable.

### Categorical Variables - 'GenreName' & 'ArtistName'

- Step 1: For these variables I'm going to count the frequency of each category across each customer. 
- Step 2: I'm then going to transform these categories into a customer - category frequency matrix. 
- Step 3: I'm going to transform these features so they follow an approximate normal distribution
- Step 4: I'm going to normalize (centre and scale) these features. 
- Step 5: Finally, because KMeans does not perform well on high dimensional data (see [k-Means Advantages and Disadvantages](https://developers.google.com/machine-learning/clustering/algorithm/advantages-disadvantages) for reference), I'm going to use [Uniform Manifold Approximation and Projection (UMAP)](https://umap-learn.readthedocs.io/en/latest/) to reduce the number of dimensions to 2.


The function below takes care of steps 1 & 2. A pipeline takes care of the rest of the steps.


```python
def to_customer_item_table(data, column):
    
    customer_item_table = data[['CustomerId', column]] \
    .value_counts(['CustomerId', column]) \
    .reset_index() \
    .pivot(
        index = 'CustomerId',
        columns = column,
        values = 0
    ) \
    .rename_axis(None) \
    .rename_axis(None, axis=1) \
    .fillna(0) \
    .rename(columns= lambda col: column + '_' + col) 
    
    customer_item_table.index.name = 'CustomerId'
    
    return customer_item_table
```

#### Genre Name


```python
# Step 1 & 2
customer_genre_table = to_customer_item_table(invoice_lines_df, 'GenreName')

# Step 3, 4 & 5
genre_pipe = make_pipeline(PowerTransformer(), StandardScaler(), UMAP(n_components=2, random_state=42))
genre_features = genre_pipe.fit_transform(customer_genre_table)

customer_genre_table.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>GenreName_Alternative</th>
      <th>GenreName_Alternative &amp; Punk</th>
      <th>GenreName_Blues</th>
      <th>GenreName_Bossa Nova</th>
      <th>GenreName_Classical</th>
      <th>GenreName_Comedy</th>
      <th>GenreName_Drama</th>
      <th>GenreName_Easy Listening</th>
      <th>GenreName_Electronica/Dance</th>
      <th>GenreName_Heavy Metal</th>
      <th>...</th>
      <th>GenreName_Pop</th>
      <th>GenreName_R&amp;B/Soul</th>
      <th>GenreName_Reggae</th>
      <th>GenreName_Rock</th>
      <th>GenreName_Rock And Roll</th>
      <th>GenreName_Sci Fi &amp; Fantasy</th>
      <th>GenreName_Science Fiction</th>
      <th>GenreName_Soundtrack</th>
      <th>GenreName_TV Shows</th>
      <th>GenreName_World</th>
    </tr>
    <tr>
      <th>CustomerId</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>14.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.0</td>
      <td>2.0</td>
      <td>9.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>17.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>17.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>15.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 24 columns</p>
</div>



First 10 rows of the clustering ready 'GenreName' data.


```python
print(genre_features[:10])
```

    [[13.044911   3.6601636]
     [13.011441   2.765037 ]
     [15.623071   0.6658808]
     [14.938987   3.08864  ]
     [15.064433   0.9512974]
     [15.852441   2.0758345]
     [14.083157   1.0859814]
     [14.003555   2.5418613]
     [13.279124   2.4457643]
     [13.550403   2.8698995]]


#### Artist Name


```python
# Step 1 & 2
customer_artist_table = to_customer_item_table(invoice_lines_df, 'ArtistName')

# Step 3, 4 & 5
artist_pipe = make_pipeline(PowerTransformer(), StandardScaler(), UMAP(n_components=3, random_state=42))
artist_features = artist_pipe.fit_transform(customer_artist_table)

customer_artist_table.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ArtistName_AC/DC</th>
      <th>ArtistName_Academy of St. Martin in the Fields &amp; Sir Neville Marriner</th>
      <th>ArtistName_Academy of St. Martin in the Fields, John Birch, Sir Neville Marriner &amp; Sylvia McNair</th>
      <th>ArtistName_Academy of St. Martin in the Fields, Sir Neville Marriner &amp; Thurston Dart</th>
      <th>ArtistName_Accept</th>
      <th>ArtistName_Adrian Leaper &amp; Doreen de Feis</th>
      <th>ArtistName_Aerosmith</th>
      <th>ArtistName_Alanis Morissette</th>
      <th>ArtistName_Alice In Chains</th>
      <th>ArtistName_Amy Winehouse</th>
      <th>...</th>
      <th>ArtistName_Toquinho &amp; Vinícius</th>
      <th>ArtistName_U2</th>
      <th>ArtistName_UB40</th>
      <th>ArtistName_Van Halen</th>
      <th>ArtistName_Various Artists</th>
      <th>ArtistName_Velvet Revolver</th>
      <th>ArtistName_Vinícius De Moraes</th>
      <th>ArtistName_Yehudi Menuhin</th>
      <th>ArtistName_Yo-Yo Ma</th>
      <th>ArtistName_Zeca Pagodinho</th>
    </tr>
    <tr>
      <th>CustomerId</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 165 columns</p>
</div>



First 10 rows of the clustering ready 'ArtistName' data.


```python
print(artist_features[:10])
```

    [[12.814907    2.0431075   1.6870314 ]
     [12.104961    2.0627768   1.7475295 ]
     [11.652204    3.268887    3.799478  ]
     [11.668995    0.76642877  3.5991812 ]
     [12.5094595   0.99819195  2.247469  ]
     [12.21816     1.1085975   3.6892366 ]
     [12.1940975   1.2894894   3.0009885 ]
     [12.489316    2.464878    3.8191035 ]
     [11.2674885   0.4835746   3.6181312 ]
     [11.646283    1.8149014   1.708857  ]]


### Numeric Variable - 'Milliseconds'

- Step 1: For each customer calculate the minimum, the 25% quantile, the 50% quantile (median), the 75% quantile, and the maximum.
- Step 2: Transform these quantiles into a customer - qunatile matrix.
- Step 3: I'm going to transform these features so they follow an approximate normal distribution
- Step 4: I'm going to normalize (centre and scale) these features. 

There is no need for dimension reduction as there are relatively few dimensions.

#### Milliseconds

The code below performs steps 1 & 2. A pipeline takes care of steps 3 & 4. 


```python
customer_milliseconds_quantile = invoice_lines_df[['CustomerId','Milliseconds']] \
    .groupby('CustomerId') \
    .quantile(q=[0.1, 0.25, 0.5, 0.75, 0.9]) \
    .reset_index() \
    .pivot(
        index = 'CustomerId',
        columns = 'level_1',
        values = 'Milliseconds'
    ) \
    .reset_index() \
    .set_axis(
        ['CustomerId', '0.0', '0.25', '0.5', '0.75', '1'],
        axis=1
    ) \
    .set_index('CustomerId') \
    .rename(columns= lambda col: 'MillisecondsQuantile_' + col)
    
customer_milliseconds_quantile.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MillisecondsQuantile_0.0</th>
      <th>MillisecondsQuantile_0.25</th>
      <th>MillisecondsQuantile_0.5</th>
      <th>MillisecondsQuantile_0.75</th>
      <th>MillisecondsQuantile_1</th>
    </tr>
    <tr>
      <th>CustomerId</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>171908.1</td>
      <td>196342.50</td>
      <td>231960.0</td>
      <td>282038.00</td>
      <td>384544.3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>146650.7</td>
      <td>208404.25</td>
      <td>233534.0</td>
      <td>277648.25</td>
      <td>368072.9</td>
    </tr>
    <tr>
      <th>3</th>
      <td>148492.6</td>
      <td>201377.25</td>
      <td>256221.5</td>
      <td>380734.25</td>
      <td>498658.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>208368.2</td>
      <td>233018.25</td>
      <td>272554.0</td>
      <td>360554.25</td>
      <td>529030.2</td>
    </tr>
    <tr>
      <th>5</th>
      <td>184267.5</td>
      <td>205720.50</td>
      <td>270833.5</td>
      <td>329567.00</td>
      <td>618323.2</td>
    </tr>
  </tbody>
</table>
</div>



First 10 rows of the clustering ready 'Milliseconds' data.


```python
milliseconds_pipe = make_pipeline(PowerTransformer(method='box-cox'), StandardScaler())
milliseconds_features = milliseconds_pipe.fit_transform(customer_milliseconds_quantile)

print(milliseconds_features[:10])
```

    [[ 0.11111969 -0.83633527 -1.0979374  -1.02137992 -0.46334155]
     [-1.10109171 -0.15428685 -1.0307586  -1.02137992 -0.64331936]
     [-1.00687014 -0.55529934 -0.06328289  1.21052435  0.3706499 ]
     [ 1.61575366  1.3297512   0.63227949  0.7641435   0.51466785]
     [ 0.6494586  -0.30864279  0.55904178  0.31776264  0.83248907]
     [-0.92946309  1.44075602  2.05219438  2.54966691  1.79904734]
     [ 1.04425042  0.66102843  0.8988359   1.21052435  1.79373918]
     [ 0.64150063  0.25298413  0.21603122 -0.12861821 -0.91099878]
     [ 0.10692681 -0.45153531 -0.60456043 -1.02137992 -0.40927931]
     [ 0.75805622  0.63453757 -0.39617841 -0.57499907 -0.16204017]]


## Saving Data

### Writing to CSV

I'll save the customer - item tables as csv files.


```python
customer_genre_table.to_csv('./00_Data/genre_clustering_data.csv')

customer_artist_table.to_csv('./00_Data/artist_clustering_data.csv')

customer_milliseconds_quantile.to_csv('./00_Data/milliseconds_clustering_data.csv')
```

### Writing to Pickle

I'll save the cluster ready numpy arrays as pickle files.


```python
pd.to_pickle(milliseconds_features, './00_Data/processed_milliseconds.py')

pd.to_pickle(genre_features, './00_Data/processed_genre.py')

pd.to_pickle(artist_features, './00_Data/processed_artist.py')
```
