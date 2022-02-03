#
# header comment? Overview, name, etc.
#

import sqlite3
import matplotlib.pyplot as figure


###########################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
  dbCursor = dbConn.cursor()
  
  print("General stats:")

  # of stations  
  dbCursor.execute("Select count(*) From Stations;")
  row = dbCursor.fetchone()
  print("  # of stations:", f"{row[0]:,}")

  # num of stops
  dbCursor.execute("Select count(*) From Stops;")
  row = dbCursor.fetchone()
  print("  # of stops:", f"{row[0]:,}")

  # num of ride entries
  dbCursor.execute("Select count(*) From Ridership;")
  row = dbCursor.fetchone()
  print("  # of ride entries:", f"{row[0]:,}")

  # date range
  dbCursor.execute("Select MIN(date(Ride_Date)), MAX(date(Ride_Date)) From Ridership;") 
  row = dbCursor.fetchone()
  print("  date range:", row[0], '-', row[1])

  # total ridership
  dbCursor.execute("Select SUM(Num_Riders) From Ridership;")
  row = dbCursor.fetchone()
  total_riders = row[0] # use this for later
  print("  Total ridership:", f"{total_riders:,}")

  # weekday ridership + percentage
  dbCursor.execute("Select SUM(Num_Riders) From Ridership Where Type_of_Day = 'W';")
  row = dbCursor.fetchone()
  weekday_riders = row[0]
  print("  Weekday ridership:", f"{weekday_riders:,}", f"({(weekday_riders/total_riders):.2%})") # print as percentage

  # saturday ridership + percentage
  dbCursor.execute("Select SUM(Num_Riders) From Ridership Where Type_of_Day = 'A';")
  row = dbCursor.fetchone()
  saturday_riders = row[0]
  print("  Saturday ridership:", f"{saturday_riders:,}", f"({(saturday_riders/total_riders):.2%})") # print as percentage

  # sunday/holiday ridership + percentage
  dbCursor.execute("Select SUM(Num_Riders) From Ridership Where Type_of_Day = 'U';")
  row = dbCursor.fetchone()
  holiday_riders = row[0]
  print("  Sunday/holiday ridership:", f"{holiday_riders:,}", f"({(holiday_riders/total_riders):.2%})") # print as percentage

# following functions are for each command

# COMMAND 1
def command_1(dbConn):
  match = input("\nEnter partial station name (wildcards _ and %): ")

  dbCursor = dbConn.cursor()
  dbCursor.execute("Select * From Stations Where Station_Name Like ? Order By Station_Name;", [match])

  rows = dbCursor.fetchall()
  
  # check if list is empty
  if not rows:
    print("**No stations found...")
  
  for r in rows:
    print(r[0], ":", r[1])

# COMMAND 2
def command_2(dbConn):
  print("** ridership all stations **")
  dbCursor = dbConn.cursor()

  # first get total number of riders
  dbCursor.execute("Select SUM(Num_Riders) From Ridership")
  total = (dbCursor.fetchone())[0]

  # get each station's ridership
  query = """
          Select Stations.Station_Name, SUM(Num_Riders) 
          From Ridership 
          Join Stations On (Ridership.Station_ID=Stations.Station_ID)
          Group By Station_Name
          Order By Station_Name;
          """
  
  dbCursor.execute(query)
  rows = dbCursor.fetchall()

  # print each row and their percentages
  for x in rows:
    num = x[1]
    print(x[0], ":", f"{num:,}", f"({(num/total):.2%})")

# COMMAND 3 
def command_3(dbConn):
  print("** top-10 stations **")
  dbCursor = dbConn.cursor()

  # first get total number of riders
  dbCursor.execute("Select SUM(Num_Riders) From Ridership")
  total = (dbCursor.fetchone())[0]

  # select top 10 busiest stations 
  query = """
          Select Stations.Station_Name, SUM(Num_Riders) as Total From Ridership JOIN Stations ON (Ridership.Station_ID=Stations.Station_ID)
          Group By Station_Name
          Order By Total DESC
          LIMIT 10;
          """
  
  dbCursor.execute(query)
  rows = dbCursor.fetchall()

  # print each row and their percentages
  for x in rows:
    num = x[1]
    print(x[0], ":", f"{num:,}", f"({(num/total):.2%})")

# COMMAND 4
def command_4(dbConn):
  print("** least-10 stations **")

  dbCursor = dbConn.cursor()

  # first get total number of riders
  dbCursor.execute("Select SUM(Num_Riders) From Ridership")
  total = (dbCursor.fetchone())[0]

  # select top 10 least-busiest stations 
  query = """
          Select Stations.Station_Name, SUM(Num_Riders) as Total From Ridership JOIN Stations ON (Ridership.Station_ID=Stations.Station_ID)
          Group By Station_Name
          Order By Total
          LIMIT 10;
          """
  
  dbCursor.execute(query)
  rows = dbCursor.fetchall()

  # print each row and their percentages
  for x in rows:
    num = x[1]
    print(x[0], ":", f"{num:,}", f"({(num/total):.2%})")

def command_5(dbConn):
  # get user input
  color = input("\nEnter a line color (e.g. Red or Yellow): ")

  dbCursor = dbConn.cursor()

  # select all stops with corresponding color
  query = """
          Select Stop_Name, Direction, ADA From Stops
          Join StopDetails On
          (Stops.Stop_ID=StopDetails.Stop_ID)
          Join Lines On (StopDetails.Line_ID=Lines.Line_ID)
          Where Color Like ?
          Order By Stop_Name;
          """

  dbCursor.execute(query, [color])
  rows = dbCursor.fetchall()

  # check if valid color
  if not rows:
    print("**No such line...")
  
  # print rows
  for x in rows:
    stop_name = x[0]
    direction = x[1]
    ada = x[2]
    a = "yes" if ada else "no"

    print(stop_name, ":", "direction =", direction, "(accessible?", a + ")")

# COMMAND 6
def command_6(dbConn):
  print("** ridership by month **")

  dbCursor = dbConn.cursor()

  # get total ridership by month
  query = """
          Select strftime('%m', Ride_Date) as Month, SUM(Num_Riders) From Ridership
          Group By Month
          Order By Month;
          """

  dbCursor.execute(query)
  rows = dbCursor.fetchall()

  x = []
  y = []

  for r in rows:
    x.append(r[0])
    y.append(r[1])
    print(r[0], ":", f"{r[1]:,}")

  plot = input("\nPlot? (y/n) ")

  if plot == "y":
    figure.xlabel("Month")
    figure.ylabel("Number of Riders (x * 10^8)")
    figure.title("Monthly Ridership")

    figure.ioff()
    figure.plot(x, y)
    figure.show(block=False)
    return

# COMMAND 7
def command_7(dbConn):
  print("** ridership by year **")

  dbCursor = dbConn.cursor()

  # get total ridership by month
  query = """
          Select strftime('%Y', Ride_Date) as Year, SUM(Num_Riders) From Ridership
          Group By Year
          Order By Year;
          """

  dbCursor.execute(query)
  rows = dbCursor.fetchall()

  x = []
  y = []

  for r in rows:
    x.append(r[0])
    y.append(r[1])
    print(r[0], ":", f"{r[1]:,}")

  plot = input("\nPlot? (y/n) ")

  if plot == "y":
    figure.xlabel("Year")
    figure.ylabel("Number of Riders (x * 10^8)")
    figure.title("Yearly Ridership")

    figure.ioff()
    figure.plot(x, y)
    figure.show(block=False)
    return

# COMMAND 8
def command_8(dbConn):
  dbCursor = dbConn.cursor()
  year = input("\nYear to compare against? ")

  # check if each station name is valid and is only 1 result
  station1 = input("\nEnter station 1 (wildcards _ and %): ")
  dbCursor.execute("Select Station_Name, Station_ID From Stations Where Station_Name Like ?", [station1])
  s1 = dbCursor.fetchall()
  if not s1:
    print("**No station found...")
    return
  elif len(s1) > 1:
    print("**Multiple stations found...")
    return
  
  # get station name
  station1 = s1[0][0]
  station1_ID = s1[0][1]

  station2 = input("\nEnter station 2 (wildcards _ and %): ")
  dbCursor.execute("Select Station_Name, Station_ID From Stations Where Station_Name Like ?", [station2])
  s2 = dbCursor.fetchall()
  if not s2:
    print("**No station found...")
    return
  elif len(s2) > 1:
    print("**Multiple stations found...")
    return
  
  # get station name
  station2 = s2[0][0]
  station2_ID = s2[0][1]

  # get daily ridership for each station
  query = """
          Select date(Ride_Date) as Date, SUM(Num_Riders) From Ridership
          Join Stations On (Ridership.Station_ID=Stations.Station_ID)
          Where Station_Name Like ? And strftime('%Y',Ride_Date) Like ?
          Group By Date
          Order By Date;
          """ 

  # get info for station1 first
  dbCursor.execute(query, [station1,year])
  rows = dbCursor.fetchall()

  x1 = []
  y1 = []

  for d in rows:
    x1.append(d[0])
    y1.append(d[1])
  
  # now get info for station2
  dbCursor.execute(query, [station2,year])
  rows = dbCursor.fetchall() 

  x2 = []
  y2 = []

  for d in rows:
    x2.append(d[0])
    y2.append(d[1])

  # print info using zip
  print("Station 1:", station1_ID, station1)
  # print first 5 and last 5 dates
  for x, y in list(zip(x1, y1))[:5]:
    print(x,y)
  
  for x, y in list(zip(x1, y1))[len(x1)-5:]:
    print(x,y)
  
  print("Station 2:", station2_ID, station2)
  for x, y in list(zip(x2, y2))[:5]:
    print(x,y)
  
  for x, y in list(zip(x2, y2))[len(x1)-5:]:
    print(x,y)
  
  plot = input("\nPlot? (y/n) ")
  if plot == "y":
    figure.xlabel("Day")
    figure.ylabel("Number of Riders")
    figure.title("Riders Each Day of " + year)

    figure.ioff()
    figure.plot(list(range(len(x1))), y1, label=station1)
    figure.plot(list(range(len(x1))), y2, label=station2)
    figure.legend()
    figure.show(block=False)
    return

# COMMAND 9
def command_9(dbConn):
  color = input("\nEnter a line color (e.g. Red or Yellow): ")

  query = """
          Select Distinct Station_Name, Stops.Latitude, Stops.Longitude From Stations 
          Join Stops On (Stations.Station_ID=Stops.Station_ID)
          Join StopDetails On (Stops.Stop_ID=StopDetails.Stop_ID)
          Join Lines On (StopDetails.Line_ID=Lines.Line_ID)
          Where Color Like ?
          Order By Station_Name;
          """
  dbCursor = dbConn.cursor()
  dbCursor.execute(query, [color])

  rows = dbCursor.fetchall()

  if not rows:
    print("**No such line...")
    return

  x = []
  y = []

  # print and populate x and y lists 
  for i in rows:
    station_name = i[0]
    latitude = i[1]
    longitude = i[2]

    print(station_name, ":", f"({latitude:.10},", f"{longitude:.10})")

    x.append(latitude)
    y.append(longitude)
  
  plot = input("\nPlot? (y/n) ")
  if plot == 'y':
    image = figure.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
    figure.imshow(image, extent=xydims)

    figure.title(color + " line")

    if (color.lower() == "purple-express"):
      color = "Purple"
    
    figure.plot(y, x, "o", c=color)

    for i in rows:
      station_name = i[0]
      latitude = i[1]
      longitude = i[2]
      figure.annotate(station_name, (longitude, latitude))

    figure.xlim([-87.9277, -87.5569])
    figure.ylim([41.7012, 42.0868])

    figure.show(block=False)

    return

# function to start command loop   
def command_loop(dbConn):
  
  while True: 
    command = input("\nPlease enter a command (1-9, x to exit): ")

    if (command == '1'):
      command_1(dbConn)
    elif (command == '2'):
      command_2(dbConn)
    elif (command == '3'):
      command_3(dbConn)
    elif (command == '4'):
      command_4(dbConn)
    elif (command == '5'):
      command_5(dbConn)
    elif (command == '6'):
      command_6(dbConn)
    elif (command =='7'):
      command_7(dbConn)
    elif (command == '8'):
      command_8(dbConn)
    elif (command =='9'):
      command_9(dbConn)
    elif (command == 'x'):
      break;
    else:
      print("**Error, unknown command, try again...")



###########################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

command_loop(dbConn);

#
# done
#
