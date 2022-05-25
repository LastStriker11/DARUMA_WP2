# DARUMA WP2 [TUM]

*Date: 03.05.2022*

------------------------------

A repository of preprocessing and previsualization codes for WP2 of the DARUMA project.

Codes for datasets from different cities can be found in the respective folders. Since all GPT data have the same format, so the codes for GPT data are shared in a public folder *GPT_codes* including a preprocessing script and a visualization notebook. In general, each dataset will be accompanied by a preprocessing script and a visualization notebook.

--------

## 1. GPT data

Please see the [codes description](GPT_codes/codes_description.md) under folder GPT_codes for more information.

## 2. Loop detector data

Loop detector data will be all transformed into tensors with the shape/dimension (# days, # detectors, # intervals in a day). The length of intervals can be changed. We apply 15 minutes now.

### 2.1 Kyoto

Only traffic counts are available.

### 2.2 Madrid

The Madrid data can be downloaded by two means: 1) downloading in real-time, which will have a 5-min interval; 2) downloading the archived version, which will have a 15-min interval. So, we have two processing scripts for Madrid data.

Besides, the real-time data has two kinds of detectors: 1) roads within Madrid; 2) inter-city motorways within the area of Madrid. The first kind of detector does not provide the speed information, while the second one provides.

### 2.3 Budapest

- The loop detector data seems to have some problems:

  - For the same detector: different time intervals (5 min) have the same value in volume, occupancy and speed.

  - At the same time interval, different detectors have the same volume, occupancy and speed.

  - The collection dates are not continuous.
  - In *Detekto_measurements_1*: one-week data are available in April, June and September of 2019;  five-day data are available in March, May, Jun and November of 2020; five-day data in June of 2021.
  - *Detekto_measurements_2* only adds the data of 'D701.1', so we do not use it.

--------------------

**Working diary**

- *23.05.2022*: processing codes for loop detector data from Madrid
- *20.05.2022*: loop detector data downloader for downloading the public detector data of Madrid.
- *18.05.2022*: preprocessing codes for loop detector data (from Kyoto and Budapest)
- *03.05.2022*: GPT data processing and visualization codes.
