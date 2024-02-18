import matplotlib.pyplot as plt
import pandas as pd

from data_gathering import carbon_dioxide_over_time
from data_gathering import energy_consumption
from data_gathering import volcano_activities
carbon_dioxide_data = carbon_dioxide_over_time.get_situ_co2_ppm()

print(carbon_dioxide_data.keys())

energy_consumption_data = energy_consumption.get_eia_us_energy_consumption()
print(energy_consumption_data.keys())

volcano_activities_data = volcano_activities.get_volcano_eruption_instances()
print(volcano_activities_data.keys())

# Convert dictionaries to pandas DataFrames
df_co2 = pd.DataFrame(carbon_dioxide_data)
df_energy = pd.DataFrame(energy_consumption_data)
df_volcanic = pd.DataFrame(volcano_activities_data)

# Interpolate missing 'ppm' values in CO2 data
df_co2['ppm'] = df_co2['ppm'].interpolate()

df_energy['cumulative_btu'] = df_energy['billion_btu'].cumsum()

# Interpolate missing 'billion_btu' values in energy consumption data
df_energy['billion_btu'] = df_energy['billion_btu'].interpolate()

# To integrate (cumulative sum) the 'instances' column of the df_volcanic dataframe,
# you can use the cumsum() method which returns the cumulative sum of the elements.

df_volcanic['cumulative_instances'] = df_volcanic['instances'].cumsum()

# Interpolate missing 'instances' values in volcanic activities data
df_volcanic['instances'] = df_volcanic['instances'].interpolate()

##################################################
# Plotting for energy consumption and CO2
##################################################

# Merge dataframes on year, month, and day
df_merged = pd.merge(df_co2, df_energy, on=['year', 'month', 'day'], suffixes=('_co2', '_energy'))

# Creating a new plot to display CO2 ppm label on the left side as well

plt.figure(figsize=(10, 6))

# Primary y-axis for CO2 ppm
ax1 = plt.gca()
ax1.plot(df_merged['year'], df_merged['ppm'], color='green', label='CO2 ppm')
ax1.set_xlabel('Year')
ax1.set_ylabel('CO2 Concentration (ppm)', color='green')
ax1.tick_params(axis='y', labelcolor='green')

# Secondary y-axis for Energy Consumption
ax2 = ax1.twinx()
ax2.plot(df_merged['year'], df_merged['billion_btu'], color='blue', label='Energy Consumption (Billion BTU)')
ax2.set_ylabel('Energy Consumption (Billion BTU)', color='blue', rotation=270, labelpad=15)
ax2.tick_params(axis='y', labelcolor='blue')

# Title
plt.title('CO2 Concentration and Energy Consumption Over Time')

# Show plot with ppm label on both sides
plt.show()

##################################################
# Plotting for energy consumption cumulative and CO2
##################################################

# Merge dataframes on year, month, and day
df_merged = pd.merge(df_co2, df_energy, on=['year', 'month', 'day'], suffixes=('_co2', '_energy_cumulative'))

# Creating a new plot to display CO2 ppm label on the left side as well

plt.figure(figsize=(10, 6))

# Primary y-axis for CO2 ppm
ax1 = plt.gca()
ax1.plot(df_merged['year'], df_merged['ppm'], color='green', label='CO2 ppm')
ax1.set_xlabel('Year')
ax1.set_ylabel('CO2 Concentration (ppm)', color='green')
ax1.tick_params(axis='y', labelcolor='green')

# Secondary y-axis for Energy Consumption
ax2 = ax1.twinx()
ax2.plot(df_merged['year'], df_merged['cumulative_btu'], color='blue', label='Energy Consumption Cumulative (Billion BTU)')
ax2.set_ylabel('Energy Consumption Cumulative (Billion BTU)', color='blue', rotation=270, labelpad=15)
ax2.tick_params(axis='y', labelcolor='blue')

# Title
plt.title('CO2 Concentration and Cumulative Energy Consumption Over Time')

# Show plot with ppm label on both sides
plt.show()

##################################################
# Plotting for Volcanic Eruptions and CO2
##################################################
# Merge CO2 data with volcanic eruption data on year, month, and day
df_merged_volcanic = pd.merge(df_co2, df_volcanic, on=['year', 'month', 'day'], suffixes=('_co2', '_instances'))

plt.figure(figsize=(10, 6))

# Primary y-axis for CO2 ppm
ax1 = plt.gca()
ax1.plot(df_merged_volcanic['year'], df_merged_volcanic['ppm'], color='green', label='CO2 ppm')
ax1.set_xlabel('Year')
ax1.set_ylabel('CO2 Concentration (ppm)', color='green')
ax1.tick_params(axis='y', labelcolor='green')

# Secondary y-axis for Volcanic Eruption Instances
ax2 = ax1.twinx()
ax2.plot(df_merged_volcanic['year'], df_merged_volcanic['instances'], color='red', label='Recorded Volcanic Eruptions')
ax2.set_ylabel('Recorded Volcanic Eruptions', color='red', rotation=270, labelpad=15)
ax2.tick_params(axis='y', labelcolor='red')

# Title and Legend
plt.title('CO2 Concentration and Volcanic Eruption Instances Over Time')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.show()

##################################################
# Plotting for Volcanic Eruptions, Cumlative and CO2
##################################################

# Then, merge df_co2 with the updated df_volcanic on year, month, and day
df_merged_cumulative_volcanic = pd.merge(df_co2, df_volcanic, on=['year', 'month', 'day'], suffixes=('_co2', '_instances_cumulative'))

plt.figure(figsize=(10, 6))

# Primary y-axis for CO2 ppm
ax1 = plt.gca()
ax1.plot(df_merged_cumulative_volcanic['year'], df_merged_cumulative_volcanic['ppm'], color='green', label='CO2 ppm')
ax1.set_xlabel('Year')
ax1.set_ylabel('CO2 Concentration (ppm)', color='green')
ax1.tick_params(axis='y', labelcolor='green')

# Secondary y-axis for Cumulative Volcanic Eruption Instances
ax2 = ax1.twinx()
ax2.plot(df_merged_cumulative_volcanic['year'], df_merged_cumulative_volcanic['cumulative_instances'], color='red', label='Cumulative Volcanic Eruptions')
ax2.set_ylabel('Cumulative Volcanic Eruptions', color='red', rotation=270, labelpad=15)
ax2.tick_params(axis='y', labelcolor='red')

# Title and Legend
plt.title('CO2 Concentration and Cumulative Volcanic Eruption Instances Over Time')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.show()