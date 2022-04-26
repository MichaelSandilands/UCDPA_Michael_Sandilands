# Specialist Certificate in Data Analytics Essentials Assignment

## Chapter 2: Merging Tables Stored in the Chinook Database

## Imports


```python
%cd ..
```

    /home/michael/Documents/python_projects/UCDPA_Michael_Sandilands



```python
import pandas as pd
import sqlalchemy as sql
```

## Import Data

The `sqlalchemy` module allows me to connect to the database through python.

### Connecting to Database


```python
engine = sql.create_engine("sqlite:///00_Data/Chinook_Sqlite.sqlite")

conn = engine.connect()
```

### Get Table Names


```python
inspector = sql.inspect(conn)

inspector.get_schema_names()
```




    ['main']




```python
table_names = inspector.get_table_names('main')

print(table_names)
```

    ['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice', 'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']


### Read the Data

I'll store all the the tables in a dictionary then use that dictionary to explore their contents. The key will be the name of the table, the value will be the table itself.


```python
data_dict = {}
for table in table_names:
    data_dict[table] = pd.read_sql(f'SELECT * FROM {table}', con=conn) 
```

### Close Connection


```python
conn.close()
```

## Combining Customer Segmentation Features

The relationships between the Chinook tables:


![Chinook Table Relationships](../00_Images/chinook-diagram.png)

We have to think about which features will be important in answering our business question. I'll use an iterator to display each table.


```python
table_itr = iter(table_names)
```


```python
data_dict[next(table_itr)].head()
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
      <th>AlbumId</th>
      <th>Title</th>
      <th>ArtistId</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>For Those About To Rock We Salute You</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Balls to the Wall</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Restless and Wild</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Let There Be Rock</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Big Ones</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



 From the 'Album' table:
- The 'Title' column may be useful.
- The 'ArtistId' column will be needed to add the 'Artist' table to the full customer segmentation data frame.


```python
data_dict[next(table_itr)].head()
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
      <th>ArtistId</th>
      <th>Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>AC/DC</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Accept</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Aerosmith</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Alanis Morissette</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Alice In Chains</td>
    </tr>
  </tbody>
</table>
</div>



From the 'Artist' table:
- The 'Name' column may be useful.


```python
data_dict[next(table_itr)].head()
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
      <th>CustomerId</th>
      <th>FirstName</th>
      <th>LastName</th>
      <th>Company</th>
      <th>Address</th>
      <th>City</th>
      <th>State</th>
      <th>Country</th>
      <th>PostalCode</th>
      <th>Phone</th>
      <th>Fax</th>
      <th>Email</th>
      <th>SupportRepId</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Luís</td>
      <td>Gonçalves</td>
      <td>Embraer - Empresa Brasileira de Aeronáutica S.A.</td>
      <td>Av. Brigadeiro Faria Lima, 2170</td>
      <td>São José dos Campos</td>
      <td>SP</td>
      <td>Brazil</td>
      <td>12227-000</td>
      <td>+55 (12) 3923-5555</td>
      <td>+55 (12) 3923-5566</td>
      <td>luisg@embraer.com.br</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Leonie</td>
      <td>Köhler</td>
      <td>None</td>
      <td>Theodor-Heuss-Straße 34</td>
      <td>Stuttgart</td>
      <td>None</td>
      <td>Germany</td>
      <td>70174</td>
      <td>+49 0711 2842222</td>
      <td>None</td>
      <td>leonekohler@surfeu.de</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>François</td>
      <td>Tremblay</td>
      <td>None</td>
      <td>1498 rue Bélanger</td>
      <td>Montréal</td>
      <td>QC</td>
      <td>Canada</td>
      <td>H2G 1A7</td>
      <td>+1 (514) 721-4711</td>
      <td>None</td>
      <td>ftremblay@gmail.com</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Bjørn</td>
      <td>Hansen</td>
      <td>None</td>
      <td>Ullevålsveien 14</td>
      <td>Oslo</td>
      <td>None</td>
      <td>Norway</td>
      <td>0171</td>
      <td>+47 22 44 22 22</td>
      <td>None</td>
      <td>bjorn.hansen@yahoo.no</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>František</td>
      <td>Wichterlová</td>
      <td>JetBrains s.r.o.</td>
      <td>Klanova 9/506</td>
      <td>Prague</td>
      <td>None</td>
      <td>Czech Republic</td>
      <td>14700</td>
      <td>+420 2 4172 5555</td>
      <td>+420 2 4172 5555</td>
      <td>frantisekw@jetbrains.com</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



From the 'Customer' table:
- For this iteration of customer segmentation I'm not going to include geographic features. These can be explored down the road, but for now I'm going to start off simple and focus on product features in order to segment customers.


```python
data_dict[next(table_itr)].head()
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
      <th>EmployeeId</th>
      <th>LastName</th>
      <th>FirstName</th>
      <th>Title</th>
      <th>ReportsTo</th>
      <th>BirthDate</th>
      <th>HireDate</th>
      <th>Address</th>
      <th>City</th>
      <th>State</th>
      <th>Country</th>
      <th>PostalCode</th>
      <th>Phone</th>
      <th>Fax</th>
      <th>Email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Adams</td>
      <td>Andrew</td>
      <td>General Manager</td>
      <td>NaN</td>
      <td>1962-02-18 00:00:00</td>
      <td>2002-08-14 00:00:00</td>
      <td>11120 Jasper Ave NW</td>
      <td>Edmonton</td>
      <td>AB</td>
      <td>Canada</td>
      <td>T5K 2N1</td>
      <td>+1 (780) 428-9482</td>
      <td>+1 (780) 428-3457</td>
      <td>andrew@chinookcorp.com</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Edwards</td>
      <td>Nancy</td>
      <td>Sales Manager</td>
      <td>1.0</td>
      <td>1958-12-08 00:00:00</td>
      <td>2002-05-01 00:00:00</td>
      <td>825 8 Ave SW</td>
      <td>Calgary</td>
      <td>AB</td>
      <td>Canada</td>
      <td>T2P 2T3</td>
      <td>+1 (403) 262-3443</td>
      <td>+1 (403) 262-3322</td>
      <td>nancy@chinookcorp.com</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Peacock</td>
      <td>Jane</td>
      <td>Sales Support Agent</td>
      <td>2.0</td>
      <td>1973-08-29 00:00:00</td>
      <td>2002-04-01 00:00:00</td>
      <td>1111 6 Ave SW</td>
      <td>Calgary</td>
      <td>AB</td>
      <td>Canada</td>
      <td>T2P 5M5</td>
      <td>+1 (403) 262-3443</td>
      <td>+1 (403) 262-6712</td>
      <td>jane@chinookcorp.com</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Park</td>
      <td>Margaret</td>
      <td>Sales Support Agent</td>
      <td>2.0</td>
      <td>1947-09-19 00:00:00</td>
      <td>2003-05-03 00:00:00</td>
      <td>683 10 Street SW</td>
      <td>Calgary</td>
      <td>AB</td>
      <td>Canada</td>
      <td>T2P 5G3</td>
      <td>+1 (403) 263-4423</td>
      <td>+1 (403) 263-4289</td>
      <td>margaret@chinookcorp.com</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Johnson</td>
      <td>Steve</td>
      <td>Sales Support Agent</td>
      <td>2.0</td>
      <td>1965-03-03 00:00:00</td>
      <td>2003-10-17 00:00:00</td>
      <td>7727B 41 Ave</td>
      <td>Calgary</td>
      <td>AB</td>
      <td>Canada</td>
      <td>T3B 1Y7</td>
      <td>1 (780) 836-9987</td>
      <td>1 (780) 836-9543</td>
      <td>steve@chinookcorp.com</td>
    </tr>
  </tbody>
</table>
</div>



From the 'Employee' table:
- I don't think sales rep. information is important in segmenting the customers.


```python
data_dict[next(table_itr)].head()
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
      <th>GenreId</th>
      <th>Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Rock</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Jazz</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Metal</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Alternative &amp; Punk</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Rock And Roll</td>
    </tr>
  </tbody>
</table>
</div>



From the 'Genre' table:
- The 'Name' column may be useful.


```python
data_dict[next(table_itr)].head()
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
      <th>InvoiceId</th>
      <th>CustomerId</th>
      <th>InvoiceDate</th>
      <th>BillingAddress</th>
      <th>BillingCity</th>
      <th>BillingState</th>
      <th>BillingCountry</th>
      <th>BillingPostalCode</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>2</td>
      <td>2009-01-01 00:00:00</td>
      <td>Theodor-Heuss-Straße 34</td>
      <td>Stuttgart</td>
      <td>None</td>
      <td>Germany</td>
      <td>70174</td>
      <td>1.98</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>4</td>
      <td>2009-01-02 00:00:00</td>
      <td>Ullevålsveien 14</td>
      <td>Oslo</td>
      <td>None</td>
      <td>Norway</td>
      <td>0171</td>
      <td>3.96</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>8</td>
      <td>2009-01-03 00:00:00</td>
      <td>Grétrystraat 63</td>
      <td>Brussels</td>
      <td>None</td>
      <td>Belgium</td>
      <td>1000</td>
      <td>5.94</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>14</td>
      <td>2009-01-06 00:00:00</td>
      <td>8210 111 ST NW</td>
      <td>Edmonton</td>
      <td>AB</td>
      <td>Canada</td>
      <td>T6G 2C7</td>
      <td>8.91</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>23</td>
      <td>2009-01-11 00:00:00</td>
      <td>69 Salem Street</td>
      <td>Boston</td>
      <td>MA</td>
      <td>USA</td>
      <td>2113</td>
      <td>13.86</td>
    </tr>
  </tbody>
</table>
</div>



From the 'Invoice' table:
- We want to pull in the 'CustomerId' column because we have to have a way to relate the 'InvoiceLine' to a sepecific customer.


```python
data_dict[next(table_itr)].head()
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
      <th>TrackId</th>
      <th>UnitPrice</th>
      <th>Quantity</th>
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
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>4</td>
      <td>0.99</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>2</td>
      <td>6</td>
      <td>0.99</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>2</td>
      <td>8</td>
      <td>0.99</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>2</td>
      <td>10</td>
      <td>0.99</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



From the 'InvoiceLine' table:
- I'll use this table as the "bottom" level for the merging process. 


```python
data_dict[next(table_itr)].head()
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
      <th>MediaTypeId</th>
      <th>Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>MPEG audio file</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Protected AAC audio file</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Protected MPEG-4 video file</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Purchased AAC audio file</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>AAC audio file</td>
    </tr>
  </tbody>
</table>
</div>




```python
data_dict[next(table_itr)].head()
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
      <th>PlaylistId</th>
      <th>Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Music</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Movies</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>TV Shows</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Audiobooks</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>90’s Music</td>
    </tr>
  </tbody>
</table>
</div>




```python
data_dict[next(table_itr)].head()
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
      <th>PlaylistId</th>
      <th>TrackId</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>3402</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>3389</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>3390</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>3391</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>3392</td>
    </tr>
  </tbody>
</table>
</div>



From the 'MediaType', 'Playlist' and 'PlaylistTrack' tables:
- I don't think this information will be important in segmenting the customers. 
- We don't care about what format the product is distributed in, the purchase of the product itself is what matters to us here.


```python
data_dict[next(table_itr)].head()
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
      <th>TrackId</th>
      <th>Name</th>
      <th>AlbumId</th>
      <th>MediaTypeId</th>
      <th>GenreId</th>
      <th>Composer</th>
      <th>Milliseconds</th>
      <th>Bytes</th>
      <th>UnitPrice</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>For Those About To Rock (We Salute You)</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>Angus Young, Malcolm Young, Brian Johnson</td>
      <td>343719</td>
      <td>11170334</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Balls to the Wall</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>None</td>
      <td>342562</td>
      <td>5510424</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Fast As a Shark</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
      <td>F. Baltes, S. Kaufman, U. Dirkscneider &amp; W. Ho...</td>
      <td>230619</td>
      <td>3990994</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Restless and Wild</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
      <td>F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. D...</td>
      <td>252051</td>
      <td>4331779</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Princess of the Dawn</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
      <td>Deaffy &amp; R.A. Smith-Diesel</td>
      <td>375418</td>
      <td>6290521</td>
      <td>0.99</td>
    </tr>
  </tbody>
</table>
</div>



From the 'Track' table:
- The 'Name' column may be useful.
- The 'Composer' column may be useful.
- The 'AlbumId' and 'GenreId' columns will be needed to merge the 'Album' and 'Genre' tables respectively to our full customer segmentation data frame.

The 'Name' column is common in a lot of tables. This column will have to be renamed as each table is joined such that it makes descriptive sense in a fully joined table.


```python
joined_df = pd.DataFrame(data_dict['InvoiceLine']) \
    .merge(
        right    = data_dict['Track'] \
            # The 'UnitPrice' column is redundant as it's already in the 'InvoiceLine' table
            .drop('UnitPrice', axis=1) \
            .rename(columns = dict(Name = 'TrackName')),
        how      = 'left',
        left_on  = 'TrackId',
        right_on = 'TrackId'
    ) \
    .merge(
        right    = data_dict['Genre'] \
            .rename(columns = dict(Name = 'GenreName')),
        how      = 'left',
        left_on  = 'GenreId',
        right_on = 'GenreId'
    ) \
    .merge(
        right    = data_dict['Album'] \
            # The 'Title' column isn't very descriptive so I'm going to prepend 'Album' to the column name
            .rename(columns = dict(Title = 'AlbumTitle')),
        how      = 'left',
        left_on  = 'AlbumId',
        right_on = 'AlbumId'
    ) \
    .merge(
        right    = data_dict['Artist'] \
            .rename(columns = dict(Name = 'ArtistName')),
        how      = 'left',
        left_on  = 'ArtistId',
        right_on = 'ArtistId'
    ) \
    .merge(
        # We only want the 'InvoiceId' and 'CustomerId' columns.
        right    = data_dict['Invoice'][['InvoiceId', 'CustomerId']],
        how      = 'left',
        left_on  = 'InvoiceId',
        right_on = 'InvoiceId'
    )

joined_df.head()

# Is 'UnitPrice' column from the 'Track' table redundent? 
# UnitPrice_Logical_Series = joined_df['UnitPrice_x'] == joined_df['UnitPrice_y']
# UnitPrice_Logical_Series.sum() # Yes DONE: edit 'Track' merge to drop 'UnitPrice' column.
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
      <th>TrackId</th>
      <th>UnitPrice</th>
      <th>Quantity</th>
      <th>TrackName</th>
      <th>AlbumId</th>
      <th>MediaTypeId</th>
      <th>GenreId</th>
      <th>Composer</th>
      <th>Milliseconds</th>
      <th>Bytes</th>
      <th>GenreName</th>
      <th>AlbumTitle</th>
      <th>ArtistId</th>
      <th>ArtistName</th>
      <th>CustomerId</th>
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
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>None</td>
      <td>342562</td>
      <td>5510424</td>
      <td>Rock</td>
      <td>Balls to the Wall</td>
      <td>2</td>
      <td>Accept</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>4</td>
      <td>0.99</td>
      <td>1</td>
      <td>Restless and Wild</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
      <td>F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. D...</td>
      <td>252051</td>
      <td>4331779</td>
      <td>Rock</td>
      <td>Restless and Wild</td>
      <td>2</td>
      <td>Accept</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>2</td>
      <td>6</td>
      <td>0.99</td>
      <td>1</td>
      <td>Put The Finger On You</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>Angus Young, Malcolm Young, Brian Johnson</td>
      <td>205662</td>
      <td>6713451</td>
      <td>Rock</td>
      <td>For Those About To Rock We Salute You</td>
      <td>1</td>
      <td>AC/DC</td>
      <td>4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>2</td>
      <td>8</td>
      <td>0.99</td>
      <td>1</td>
      <td>Inject The Venom</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>Angus Young, Malcolm Young, Brian Johnson</td>
      <td>210834</td>
      <td>6852860</td>
      <td>Rock</td>
      <td>For Those About To Rock We Salute You</td>
      <td>1</td>
      <td>AC/DC</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>2</td>
      <td>10</td>
      <td>0.99</td>
      <td>1</td>
      <td>Evil Walks</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>Angus Young, Malcolm Young, Brian Johnson</td>
      <td>263497</td>
      <td>8611245</td>
      <td>Rock</td>
      <td>For Those About To Rock We Salute You</td>
      <td>1</td>
      <td>AC/DC</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



## Dropping Unnecessary Columns

We want to drop the columns that end with 'Id' except for the columns that start with 'Invoice' or 'Customer' 


```python
final_joined_df = joined_df.loc[:, joined_df.columns.str.contains('^Invoice|^Customer|(?<!Id)$')]

final_joined_df.head()
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
      <th>UnitPrice</th>
      <th>Quantity</th>
      <th>TrackName</th>
      <th>Composer</th>
      <th>Milliseconds</th>
      <th>Bytes</th>
      <th>GenreName</th>
      <th>AlbumTitle</th>
      <th>ArtistName</th>
      <th>CustomerId</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>0.99</td>
      <td>1</td>
      <td>Balls to the Wall</td>
      <td>None</td>
      <td>342562</td>
      <td>5510424</td>
      <td>Rock</td>
      <td>Balls to the Wall</td>
      <td>Accept</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>0.99</td>
      <td>1</td>
      <td>Restless and Wild</td>
      <td>F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. D...</td>
      <td>252051</td>
      <td>4331779</td>
      <td>Rock</td>
      <td>Restless and Wild</td>
      <td>Accept</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>2</td>
      <td>0.99</td>
      <td>1</td>
      <td>Put The Finger On You</td>
      <td>Angus Young, Malcolm Young, Brian Johnson</td>
      <td>205662</td>
      <td>6713451</td>
      <td>Rock</td>
      <td>For Those About To Rock We Salute You</td>
      <td>AC/DC</td>
      <td>4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>2</td>
      <td>0.99</td>
      <td>1</td>
      <td>Inject The Venom</td>
      <td>Angus Young, Malcolm Young, Brian Johnson</td>
      <td>210834</td>
      <td>6852860</td>
      <td>Rock</td>
      <td>For Those About To Rock We Salute You</td>
      <td>AC/DC</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>2</td>
      <td>0.99</td>
      <td>1</td>
      <td>Evil Walks</td>
      <td>Angus Young, Malcolm Young, Brian Johnson</td>
      <td>263497</td>
      <td>8611245</td>
      <td>Rock</td>
      <td>For Those About To Rock We Salute You</td>
      <td>AC/DC</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



Let's break down this regex:
- '^Invoice': starts with 'Invoice'.
- '^Customer': starts with 'Customer'.
- '(?<!Id)$': Negative look-behind. What immediately precedes the end of the string is not 'Id'.
- '|': Either or.
- In plain english: Keep the columns that starts with 'Invoice' or starts with 'Customer' or does not end with 'Id'.

## Relocating Columns

I personally prefer to have the 'Id' columns at the front of the data frame


```python
cols_list = final_joined_df.columns.tolist()

cols_to_front = [col for col in cols_list if 'Id' in col]
cols_remaining = [col for col in cols_list if col not in cols_to_front]

invoice_lines_df = final_joined_df[[*cols_to_front, *cols_remaining]]

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
      <td>None</td>
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




```python
print(invoice_lines_df.info())
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 2240 entries, 0 to 2239
    Data columns (total 12 columns):
     #   Column         Non-Null Count  Dtype  
    ---  ------         --------------  -----  
     0   InvoiceLineId  2240 non-null   int64  
     1   InvoiceId      2240 non-null   int64  
     2   CustomerId     2240 non-null   int64  
     3   UnitPrice      2240 non-null   float64
     4   Quantity       2240 non-null   int64  
     5   TrackName      2240 non-null   object 
     6   Composer       1644 non-null   object 
     7   Milliseconds   2240 non-null   int64  
     8   Bytes          2240 non-null   int64  
     9   GenreName      2240 non-null   object 
     10  AlbumTitle     2240 non-null   object 
     11  ArtistName     2240 non-null   object 
    dtypes: float64(1), int64(6), object(5)
    memory usage: 227.5+ KB
    None


## Writing to CSV


```python
invoice_lines_df.to_csv('./00_Data/invoice_lines.csv', index=False)
```
