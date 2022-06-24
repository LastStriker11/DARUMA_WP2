# DARUMA WP2

*Date: 03.05.2022*

------------------------------

A repository of preprocessing and previsualization codes for WP2 of the DARUMA project.

Codes for datasets from different cities can be found in the respective folders. Since all GPT data have the same format, so the codes for GPT data are shared in a public folder *GPT_codes* including a preprocessing script and a visualization notebook. In general, each dataset will be accompanied by a preprocessing script and a visualization notebook.

--------
## 1. Data in common

### 1.1 GPT data

Please see the [codes description](GPT_codes/codes_description.md) under folder GPT_codes for more information.

### 1.2 Loop detector data

Loop detector data will be all transformed into tensors with the shape/dimension (# days, # detectors, # intervals in a day). The length of intervals can be changed. We apply 15 minutes now.

#### 1.2.1 Kyoto

Only traffic counts are available.

#### 1.2.2 Madrid

The Madrid data can be downloaded by two means: 1) downloading in real-time, which will have a 5-min interval; 2) downloading the archived version, which will have a 15-min interval. So, we have two processing scripts for Madrid data.

Besides, the real-time data has two kinds of detectors: 1) roads within Madrid; 2) inter-city motorways within the area of Madrid. The first kind of detector does not provide the speed information, while the second one provides.

#### 1.2.3 Budapest

- The loop detector data seems to have some problems:

  - For the same detector: different time intervals (5 min) have the same value in volume, occupancy and speed.
  - At the same time interval, different detectors have the same volume, occupancy and speed.
  - The collection dates are not continuous.
  - In *Detekto_measurements_1*: one-week data are available in April, June and September of 2019;  five-day data are available in March, May, Jun and November of 2020; five-day data in June of 2021.
  - *Detekto_measurements_2* only adds the data of 'D701.1', so we do not use it.

### 1.3 Twitter data

The codes for combining twitter data samples are available in `Twitter_codes/twitter_data_processing.py`. The program was created based on the samples provided by Kyoto, but the data format should be the same among the three cities, so all cities should be able to process the data with the same code. Since the format of twitter data is already kind of ready to use, we just separate the information about tweets and the information about users in this processing program.

(Remark: the "keyword based" samples provided by Kyoto should be able to use directly without further processing)

## 2. Budapest data

### 2.1 TomTom data

There are two kinds of TomTom data, one is OD matrix which does not need further processing (in the folders start with *od_*, e.g., *od_20220307_20220313*), and another one is the link-based data which measuring the average travel time and speed, and aggregated counts of FCD vehicles (in the folders start with *district*, e.g., *district11_20220103_20220109*).

Regarding the first dataset:

- Each file contains the hourly OD data within 7-10 and 15-18 of several days. So, some data are duplicates. For example, in folder *od_20220307_20220313*, only two unique files.
- Need to confirm with partners from Budapest.

Regarding the second dataset:

- creationTime
- network
  - segmentResults: includes the data of 3002 link segments, each segment includes the following data.
    - distance: length of the link
    - newSegmentId
    - shape
    - segmentTimeResults: includes the average speed, travel time, and number of FCD vehicles from 4:00-10:00 with a 15-min interval (24 intervals in total).
- timeSets
  - ID from 2 to 25. 2 represents the time 4:00-4:15, and 25 represents 9:45-10:00.

After processing, we will get the data of 3002 links within the district 11 of Budapest, including:

- The link related information (`Budapest/codes/results/TomTom_link_info.csv`), including ID, speed limit and length
- average speed of probes (one csv file each date, in `Budapest/codes/results/TomTom`)
- number of probes passing through (one csv file each date)
- average travel time

## 3. Kyoto data
### 3.1 docomo data
It contains two datasets. One is for OD flows, and another one is for population. Both datasets will be converted to tensor format with the shape/dimension (# time intervals, # OD pairs,  # variables) by running `Kyoto/codes/docomo_data_processing.py`. But, the "stay" dataset needs an additional area ID table for this purpose.

Regarding the "OD" dataset:

- updated every 3 hours
- 1km * 1km
- three aggregation ways are provided as described in `OD/00_README.xlsx` (each one will have a specific tensor)

Regarding the "stay" dataset:

- updated every hour
- 500m * 500m
- four aggregation ways are provided as described in `stay/00_README.xlsx` (each one will have a specific tensor)

### 3.2 Wi-Fi data



--------------------

**Working diary**

- *10.06.2022*： codes for processing Budapest TomTom data.
- *23.05.2022*: processing codes for loop detector data from Madrid.
- *20.05.2022*: loop detector data downloader for downloading the public detector data of Madrid.
- *18.05.2022*: preprocessing codes for loop detector data (from Kyoto and Budapest)
- *03.05.2022*: GPT data processing and visualization codes.
