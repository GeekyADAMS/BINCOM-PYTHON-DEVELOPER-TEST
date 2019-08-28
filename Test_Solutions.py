# import all needed modules and libraries
import re, operator, psycopg2 as pg2, pandas as pd, random


# HTML COLOR TASK
with open(r"python_class_test.html", 'r') as html_doc: #open html file and save as html_doc
    html = html_doc.read() #read html content

color_list = re.findall(r"<td>(.*)</td>", html) # regex to collect everything between td tags

# iterate to remove days from color list
for color in color_list:
    if color == "MONDAY" or color == "TUESDAY" or color == "WEDNESDAY" or color == "THURSDAY" or color == "FRIDAY":
        color_list.remove(color)

# Fine tune list items by joining to make one list item, and splitting to get each iten
newerList = str(",".join(color_list))
newestList = newerList.split(",")
confirmList = []

# Iterate to strip each element of space and get exact color value
for element in newestList:
    col = element.strip()
    confirmList.append(col)
confirmList.remove("") # remove space item in color list
print(confirmList)

color_count = {} # create empty dictionary

# iterate confirmList to pick each color, count occurence and map occurence to the color
# which is then added to dictionary
for item in confirmList:
    count = confirmList.count(item)
    color_count[item] = count
print(color_count)

color_count_values = color_count.values() # get all dictionary keys for future use
color_count_keys = color_count.keys() # get all dictionary values for future use

# mean = sum of all color counts divided by number of distinct colors in dictionary
mean = int(sum(color_count_values) / len(color_count_values))
print(color_count_values)

# print mean value depending on match with color in dictionary
if mean in color_count_values:
    print("\nThe mean color of shirt is: ", list(color_count.keys())[list(color_count_values).index(mean)], " = ", mean)
else:
    print("\nThe mean color of shirt is: ", list(color_count.keys())[list(color_count_values).index(mean+1)], " \n")

# max value in dictionary using operator module
print("The color worn mostly throughout the week is " + max(color_count.items(), key=operator.itemgetter(1))[0])

rearrangement = sorted(color_count_values)  # re-arrange dictionary values to get median
mid = int(len(rearrangement)/2)  # get mid position

# get median value by using media formula (get middle directly if lenth of item is odd,
# otherwise, add up elements in middle and divide by 2)
if len(rearrangement)%2 != 0:
    median = rearrangement[mid]
    print("\nThe median color is :", median)
else:
    median = (rearrangement[mid] + rearrangement[mid - 1]) / 2
    print("\nThe median color is :", median)

# create mean deviation list for each color item
mean_deviations = []
# deviation = mean minus item value
for number in color_count_values:
    mean_deviations.append((number-mean)**2)

# variance = "summation of each color mean deviations divided by length of the number of colors"
variance = sum(mean_deviations)/(len(color_count_values))
print("\nThe variance of the colors is: ", variance)

# print probabilty of red === red count divided by the total colors count
print("\nThe probability of picking RED at random from the colors is: ", color_count["RED"]/sum(color_count_values), "\n")


# POSTGRES TASK

# collect database details from user
database = input("Enter your database name e.g. postgres: ")
username = input("Enter your database username e.g. postgres: ")
password = input("Enter your database password: ")

# establish database connection with detail provided
conn = pg2.connect(
    database=database,
    user=username,
    password=password,
    host="127.0.0.1",
    port="5432"
)

# create cursor for executions
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS color_data''') # delete table if table already exists

# create table with name color_data with columns colors and color_frequency
cur.execute(
    '''CREATE TABLE color_data (colors VARCHAR NOT NULL, color_frequency VARCHAR NOT NULL)'''
)

# iterate through each color in dictionary and insert its detains in table created
for colourItem in color_count_keys:
    cur.execute('''INSERT INTO color_data (colors, color_frequency) VALUES (%s, %s)''',
                (colourItem, color_count[colourItem]))

# read sql table and print the table using pandas
table = pd.read_sql('''SELECT * from color_data''', conn)
print(table, "\n")

conn.commit() # commit all operations into database
cur.close() # close cursor to avoid any mis-happenings
conn.close() # close connection to database


# CUSTOM USER SEARCH
List = [2, 5, 7, 2, 93, 783, 57, 21, 54, 12, 2, 1, 3, 11] # define list
userInt = int(input("Enter number to search: ")) # collect user input
found = 0

# iterate through list to see if user entry match any item in list
for num in List:
    if userInt == num:
        found += 1
if found != 0:
    print("\nNumber was found in list.\n") # print match if match
elif found == 0:
    print("\nNumber not found in list.\n") # print unmatch if user entry does not match any list item

# BINARY CONVERSION TASK

binaryString = ""

for i in range(0, 4): # iterate to get 4 random number between 0 and 1
    number = random.choice(range(0, 2)) # generate random number which can be 0 or 1
    binaryString += str(number) # add generated number it to a binary string

decimal = int(binaryString, 2) # convert string containing binary sequence to decimal
print("The generated binary is: ", binaryString)
print("Its equivalent decimal is: ", decimal)


# FIBONACCI TASK
nth_term = 50 # define fibonacci sequence length
# define first and second number which are usually 0 and 1 respectively unless specified
first_number = 0
second_number = 1
fibonacci_list = [first_number, second_number] # define fibonacci list with 0 and 1 as items already
i = 0

while i < nth_term-2: # iterate in range length of fibonacci sequence minus initial 0 and 1
    z = first_number + second_number # next number = summation of the current number and previous number
    fibonacci_list = fibonacci_list + [z] # add next number to the fibonacci list
    # previous number becomes current number and next number becomes current number
    first_number = second_number
    second_number = z
    i += 1

print("\nFirst 50 Fibonacci series are: ", fibonacci_list)
print("The sum of the first 50 Fibonacci series is: ", sum(fibonacci_list))


# Binary search and replace task
pattern = "0101101011101011011101101000111"
regX = re.sub("[^(11{0,1})]", "0", pattern)
newReg = re.sub("11{2}", "001", regX)

print("\n", regX)
print("0000000000100000000100000000001")
