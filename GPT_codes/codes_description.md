# DARUMA (WP2): codes for GPT data

*Contact: qinglong.lu@tum.de*

**Date: 2022-03-04**

-------

## 1. Data processing and cleaning

The *data_preprocessing.py* is used for this task.

### 1.1 Preparation

- An *output* folder should be created in a folder one level above the folder where the program is located to store the data. Otherwise, the user needs to change the path at line 15 to the corresponding folder.
- A *results* folder should be created in the same folder of the program to store the output. Otherwise, the user needs to change the path at line 247 accordingly.
- The name of the GPT data file should with the format '*popularity_\<date\>-\<time\>.csv*'. Otherwise, the user needs to modify line 37 and line 38 accordingly. If we are all using the downloader provided by Vishal Mahajan (TUM), the name format should be the same.

### 1.2 Function introduction

We have five functions in this program.

- `data_info_stat()`: Summarize the information of all downloaded data, including:
  - Name of the file
  - Week of year the data belongs to
  - day of week the data belongs to
  - time of day (hour) the data belongs to
- `gpt_list2df()`: Convert the raw popularity data (in dictionary) to pandas dataframe. Nan data pieces are also cleaned.
  - Input: result from `data_info_stat()`.
  - Output: A dataframe containing all historical GPT data listed in the *'../output/'* folder. The dimension should be (\<# records\>, 169). 169 consists of 168 (24*7) columns for hours in a week and one column for the **week of year** that the record belongs to.
- `gpt_clean()`: Cleaning the GPT data.
  - Input: results from `data_info_stat()`and `gpt_list2df()`.
  - Output: A list of dataframes. Each dataframe contains the data of one week. Thus, the dimension should be (\<# of venues\>, 168). The length of the list then is the number of weeks that data have been downloaded.
  - Cleaning steps:
    - Delete duplicates (some records are the same).
    - Delete records with all 0.
    - Delete POIs without updating historical data at lease once a week. i.e., only POIs that update the historical popularity once a week are preserved.
    - Delete outliers (interquartile range). **You can commented it if you don't need it.**
    - Average values for those updating GPT **more** than once a week.
- `gpt_day_wise()`: Rearrange the data based on the day of week.
  - Input: result from `gpt_clean()`.
  - Output: A list of sub-lists. Each sub-list consists of dataframes. Each dataframe contains the data of that day. The dimension of one dataframe is thus  (\<# of venues\>, 24). The length of the sub-list is the number of weeks. The length of the list is 7 (seven days a week. 0:Mon -> 6:Sun).
- `gpt_real_time()`: Process the real-time popularity (i.e., current popularity) data.
  - Stations have been excluded, but the user can remove this filtering step by changing line 208 accordingly.
  - Output: A dataframe of real-time popularity. The dimension should be (\<# of venues with popularity data\>, \<# of hours\>).

### 1.3 Output

The result will be stored in *'results/data_processed.pckl'* with the following order:

- Result from `gpt_clean()`
- Result from `gpt_day_wise()`
- Result from `gpt_real_time()`
- POIs that have historical data in all weeks.
- Result from `data_info_stat()`
- Other info the venues, including: lat, lon, node type, rating, rating number.

## 2. Data visualization

The *GPT_visualization.ipynb* notebook is used for this task. The user can use to draw heatmaps of historical data and compare the changes of average popularity within a day (weekday, Saturday, or Sunday). Examples are given as below.

- *heatmap_hour_venue*.pdf: Heatmap with x axis as the time of  a week and the y axis as the order of venues
- *heatmap_hour_day.pdf*: Heatmap with x axis as the time of day and the y axis as the order of days
- *average_pattern.pdf*: Comparison of changes in popularity within a day
- *average_pattern_nozeros.pdf*: Comparison of changes in popularity within a day (after dropping the rows with all zeros)



