# Analyzing the CTA Database 
*Chicago Transit Authority (CTA)*

This is a command-line interface (CLI) that offers various commands (1-9) to query the public CTA database such as ridership, station names, and more.

Technologies used: python, sqlite3, matplotlib

Below details all of the commands available:

| Command | Description |
| --- | --- |
| 1 | Searches for a station name and returns any station name that matches (using SQL wildcards _ and % are valid) |
| 2 | Prints the total ridership of each station |
| 3 | Outputs the top 10 **most** busiest stations in terms of ridership (descending) |
| 4 | Outputs the top 10 **least** busiest stations in terms of ridership (ascending) |
| 5 | Takes in one of the 8 train lines (Red, Blue, Brown, etc.) as input and lists every station associated with that line |
| 6 | Outputs total CTA ridership by month (ascending) and gives an option to plot the data (via `matplotlib.pyplot`) |
| 7 | Outputs total CTA ridership by year (ascending) and gives an option to plot the data |
| 8 | Takes a year and two station names as input and outputs daily ridership for each station that year. Also gives the option to plot both stations (using SQL wildcards _ and % are valid) |
| 9 | Takes a train line as input and outputs all station names that are part of that line (ascending). Gives the option to plot the locations as an overlay on a map of Chicagoland | 
