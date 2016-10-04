1. How would your design change if the data was not static (i.e updated frequently
during the day)?

Move the shop_data to a separate component. This component reloads its data when the csv files change (file watcher).
Care needs to be taken to ensure availability of the API during reloads of the csv files (failover, retry, caching).
At the moment, the sorting by popularity is done once on data load to speed up each individual search.

2. Do you think your design can handle 1000 concurrent requests per second? If not, what
would you change?

The data is stored in memory rather than being read off disk.
If the memory capacity is adequate, this will be much faster than disk I/O (reading off disk for each request).
A database with a good index would make each search quicker.
At the moment it is synchronous, so each request must complete before the next can start.
This will cause problems with many concurrent requests.