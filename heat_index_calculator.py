# HEAT INDEX CALCULATOR

# Code development for this calculator took place in the Jupyter Notebook "head_index_calculator.ipynb",
# which is part of this repository.
# The final code was added to this script to make it easily executable.

# Sources:
# NWS WPC "The Heat Index Equation": https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
# University of Miami, Brian McNoldy "Calculate Temperature, Dewpoint, or Relative Humidity": University of Miami (https://bmcnoldy.earth.miami.edu/Humidity.html) 

# User inputs = temperature and dew point in either degrees C or degrees F

# Import necessary modules
import math

# Request user inputs
temp = input("Enter the air temperature as a whole number, in degrees C or degrees F) \n")
temp = int(temp)
dewpt = input("Enter the dew point temperature as a whole number, in degrees C or degrees F) \n")
dewpt = int(dewpt)
t_scale = input("Are the temperature and dew point in degrees Celcius or degrees Fahrenheit? Enter 'C' for Celcius or 'F' for Fahrenheit) \n")

# Print out the variables the user entered (confirmation)
print ("You entered:")
print("temp = ", temp)
print("dewpt = ", dewpt)
print("temperature scale = ", t_scale)

# The HI formulas require temp and dewpt in Fahrenheit, whereas the RH forumula requires temp and dewpt in Celcius, 
# so save the temp and dewpt in both F and C

# Possible error: this code assumes that the user correctly entered the temp scale as either F or C
# I'm not including error handling for any other possible value of t_scale 

# If temp and dewpt were entered in Fahrenheit, convert to Celcius
if t_scale == 'F':
    tempF = temp
    dewptF = dewpt

    tempC = round((tempF - 32)*(5/9),1)
    dewptC = round((dewptF - 32)*(5/9),1)

# If temp and dewpt were entered in Celcius, convert to Fahrenheit
else:
    tempC = temp
    dewptC = dewpt

    tempF =(tempC*(9/5)) + 32
    dewptF = (dewptC*(9/5)) + 32

# Calculate RH using temp and dewpt (in C)
rh =round(100*(math.exp((17.625*dewptC)/(243.04+dewptC))/math.exp((17.625*tempC)/(243.04+tempC))),2)
print("\n At this temperature and dewpoint, the relative humidity is ", rh, "%")

# Calculate HI using simple forumula
# If this formula returns an HI > 80F, we need to use the full regression

# Units:
# temp and dewpt must be in degrees F
# rh must be in percent

heat_index_simp = round(0.5 * (tempF + 61.0 + ((tempF-68.0)*1.2) + (rh*0.094)),0)

# If the simple HI formula returns a value less than 80 degrees, we're done:
if heat_index_simp < 80:
    heat_index = heat_index_simp

else: 
    heat_index_reg = round((-42.379) + (2.04901523*tempF) + (10.14333127*rh) 
                       - (.22475541*tempF*rh) - (.00683783*tempF*tempF) 
                       - (.05481717*rh*rh) + (.00122874*tempF*tempF*rh) 
                       + (.00085282*tempF*rh*rh) - (.00000199*tempF*tempF*rh*rh),0)
    
    # apply any applicable adjustments
    if (rh < 13) and ((tempF > 80) and (tempF < 112)):
        adj1 = ((13-rh)/4)*math.sqrt((17-abs(tempF-95))/17)

        heat_index_reg = round(heat_index_reg - adj1,0)

    if (rh > 85) and ((tempF > 80) and (tempF < 87)):
        adj2 = ((rh-85)/10) * ((87-tempF)/5)

        heat_index_reg = round(heat_index_reg + adj2,0)
    
    heat_index = heat_index_reg

print("\nThe heat index under these conditions is ", heat_index, "degrees Fahrenheit")

# Specify by how much the humidity raises the apparent temperature - i.e. how much higher is the HI than the air temp

t_diff = round(heat_index - tempF,0)
print ("The humidity in the air makes it feel", t_diff, "degrees warmer than the air temperature. \n")