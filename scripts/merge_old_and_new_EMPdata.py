import numpy as np 
import pandas as pd 


new_data = pd.read_csv('../sources/SACSJ_delta_water_quality_2012_2018.csv') 
datafile = open('../sources/EMP_Lab_updated.csv', 'a')

numdict ={0: 'TotPhos', 1: 'TKN', 2:'DissOrthoPhos', 3: 'Chla', 4: 'TSS', 5: 'TDS', 6: 'DON', 7: 'DissAmmonia', 8: 'DissNitrateNitrite', 9:'DissSilica'}
dict = {'TotPhos':'Phosphorus (Total)', 'TKN':'Kjeldahl Nitrogen (Total)', 'DissOrthoPhos': 'Ortho-phosphate (Dissolved)',
		'Chla': 'Chlorophyll a', 'TSS': 'Solids (Total Suspended)', 'TDS': 'Solids (Total Dissolved)', 
		'DON': 'Organic Nitrogen (Dissolved)', 'DissAmmonia': 'Ammonia (Total)', 'DissNitrateNitrite': 'Nitrite + Nitrate (Dissolved)',
		'DissSilica': 'Silica (SiO2) (Dissolved)'}

### find index for 2012 data and just do from there to the end

for i in range(len(new_data)):
	for k in range(len(dict)):
		datafile.write("EMP Monitoring,Discrete WQ,")
		datafile.write("%s," % (new_data['Station'][i]))
		datafile.write("%f," % (new_data['Depth'][i]))
		datafile.write("%s," % (new_data['Date'][i]))
		datafile.write("%s," % (dict[numdict[k]]))
		datafile.write("=,%s,mg/L,,,Nutrients\n" % new_data[numdict[k]][i])

datafile.close()


datafile = open('../sources/EMP_Field_updated.csv', 'a')

numdict = {0:'Secchi', 1:'WTSurface', 2:'DOSurface', 3:'TurbiditySurface', 4:'pHSurface', 5:'SpCndSurface'}
dict = {'Secchi': 'Secchi Depth', 'WTSurface': 'Temperature', 'DOSurface': 'Oxygen',
		'TurbiditySurface':'Turbidity', 'pHSurface':'pH', 'SpCndSurface': 'Conductance (EC)'}

for i in range(len(new_data)):
	for k in range(len(dict)):
		datafile.write("EMP Monitoring,")
		datafile.write("%s," % new_data['Date'][i])
		datafile.write("%s," % new_data['Station'][i])
		datafile.write("%s,,," % new_data['Depth'][i])
		datafile.write("%f," % new_data[numdict[k]][i])
		datafile.write("Water,,,%s," % dict[numdict[k]])
		datafile.write(",,\n")

datafile.close()