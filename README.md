# DARUMA WP2 [TUM]

*Date: 03.05.2022*

------------------------------

A repository of preprocessing and previsualization codes for WP2 of the DARUMA project.

Codes for datasets from different cities can be found in the respective folders. Since all GPT data have the same format, so the codes for GPT data are shared in a public folder *GPT_codes* including a preprocessing script and a visualization notebook. In general, each dataset will be accompanied with a preprocessing script and a visualization notebook.

Some important notes are given below:

- Loop detector data will be all transformed into tensors with the shape/dimension (# days, # detectors, # intervals). The length of intervals can be specified in the codes. We apply 10 minutes now.

----------------------------

## 1. Kyoto data

## 2. Madrid data

## 3. Budapest data

- The loop detector data seems to have some problems:

  - For the same detector: different time intervals (5 min) have the same value in volume, occupancy and speed.

  - At the same time interval, different detectors have the same volume, occupancy and speed.

  - The collection dates are not continuous.
  - In *Detekto_measurements_1*: one-week data are available in April, June and September of 2019;  five-day data are available in March, May, Jun and November of 2020; five-day data in June of 2021.
  - In *Detekto_measurements_2 only adds the data of 'D701.1'.

--------------------

**Working diary**

- *22.05.2022*: upload the loop detector data downloader for downloading the public detector data of Madrid.
- *20.05.2022*: upload the preprocessing codes for loop detector data (from Kyoto and Budapest)
- *03.05.2022*: upload the GPT data processing codes and corresponding codes explanation.
