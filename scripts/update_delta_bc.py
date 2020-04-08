import numpy as np 
import pandas as pd 
from pycurrents.plot.maptools import mapper
import matplotlib.pyplot as plt
from stompy.io.local import usgs_nwis



stations = pd.read_csv('../sources/EMP_Discrete_Water_Quality_Stations.csv') 
data = pd.read_csv('../sources/SACSJ_delta_water_quality_2000_2018.csv') 
data['Date'] = pd.to_datetime(data['Date'])

sac_flow = pd.read_csv('../sources/sac_flow.csv')
sac_flow['Date'] = pd.to_datetime(sac_flow['Date'])
sj_flow = pd.read_csv('../sources/sj_flow.csv')
sj_flow['Date'] = pd.to_datetime(sj_flow['Date'])

false_sac = pd.read_csv('../outputs/intermediate/false_sac.csv')
false_sac['Date'] = pd.to_datetime(false_sac['Date'])
false_sj = pd.read_csv('../outputs/intermediate/false_sj.csv')
false_sj['Date'] = pd.to_datetime(false_sj['Date']) 

start_date = np.datetime64('2016-10-01')
end_date = np.datetime64('2018-12-01')

if 0:
	fig, ax = plt.subplots()
	m = mapper([-121, -123], [37, 38.5])
	m.topo()
	m.grid()
	colors = ['tab:blue', 'tab:orange', 'tab:green','tab:red', 'tab:purple', 'tab:brown', 'tab:pink',
			  'black', 'lightcoral', 'peachpuff', 'goldenrod', 'olivedrab', 'yellowgreen', 'darkseagreen', 'mediumseagreen', 'turquoise',
			  'lightseagreen', 'darkslategrey', 'teal', 'cadetblue', 'steelblue', 'cornflowerblue', 'midnightblue', 'slateblue', 
			  'darkslateblue', 'mediumvioletred', 'pink']
	for i in range(len(stations.Station.values)):
		m.mplot(stations.Longitude.values[i], stations.Latitude.values[i], linestyle='None', marker='^', color=colors[i], alpha=0.8, label=stations.Station.values[i])
	ax.legend()

stat = stations.Station.values
lat = stations.Latitude.values
lon = stations.Longitude.values

if 0: ## check start and end dates of stations
	for s in stat:
		ind = np.where(data.Station==s)[0]
		if len(ind)>0:
			start_date = data.Date.values[ind][0]
			end_date = data.Date.values[ind][-1]
			print("%s: %s, %s" %(s, str(start_date), str(end_date)))

# stations with 2016+ data
valid_stations = ['C3A', 'D22', 'D26', 'D41', 'D6', 'D7', 'D8', 'MD10A', 'NZ002',
				  'NZ004', 'NZS42', 'C9', 'D24']
sind = [np.where(stat==s)[0][0] for s in valid_stations]

if 0:
	fig, ax = plt.subplots()
	m = mapper([-121, -123], [37, 38.5])
	m.topo()
	m.grid()
	colors = ['tab:blue', 'tab:orange', 'tab:green','tab:red', 'tab:purple', 'tab:brown', 'tab:pink',
			  'black', 'lightcoral', 'peachpuff', 'goldenrod', 'olivedrab', 'yellowgreen', 'darkseagreen', 'mediumseagreen', 'turquoise',
			  'lightseagreen', 'darkslategrey', 'teal', 'cadetblue', 'steelblue', 'cornflowerblue', 'midnightblue', 'slateblue', 
			  'darkslateblue', 'mediumvioletred', 'pink']
	for i in range(len(valid_stations)):
		m.mplot(stations.Longitude.values[sind[i]], stations.Latitude.values[sind[i]], linestyle='None', marker='^', color=colors[sind[i]], alpha=0.8, label=stations.Station.values[sind[i]])
	ax.legend()


# stations with 2017 data
valid_stations = ['C3A', 'D22', 'D26', 'D8', 'MD10A', 'NZ002','NZS42', 'C9']
sind = [np.where(stat==s)[0][0] for s in valid_stations]

if 0:
	fig, ax = plt.subplots()
	m = mapper([-121, -123], [37, 38.5])
	m.topo()
	m.grid()
	colors = ['tab:blue', 'tab:orange', 'tab:green','tab:red', 'tab:purple', 'tab:brown', 'tab:pink',
			  'black', 'lightcoral', 'peachpuff', 'goldenrod', 'olivedrab', 'yellowgreen', 'darkseagreen', 'mediumseagreen', 'turquoise',
			  'lightseagreen', 'darkslategrey', 'teal', 'cadetblue', 'steelblue', 'cornflowerblue', 'midnightblue', 'slateblue', 
			  'darkslateblue', 'mediumvioletred', 'pink']
	for i in range(len(valid_stations)):
		m.mplot(stations.Longitude.values[sind[i]], stations.Latitude.values[sind[i]], linestyle='None', marker='^', color=colors[sind[i]], alpha=0.8, label=stations.Station.values[sind[i]])
	ax.legend()


######## conversions ########
#	NH4 = TKN – DON
#	NO3 = NO3 + NO2 
#	PO4 = Dissolved OrthoP
#############################

## D22 and D26

### use D24 for Sacramento 2016 data and D22 for 2017 data
s = 'D24'
ind = np.where(data.Station==s)[0]

time1 = data.Date.values[ind]
TKN1 = data.TKN.values[ind].astype(float)
DON1 = data.DON.values[ind].astype(float)
NH41 = TKN1 - DON1
NO31 = data.DissNitrateNitrite.values[ind].astype(float)
PO41 = data.DissOrthoPhos.values[ind].astype(float)

s = 'D22'
ind = np.where(data.Station==s)[0]

n = -12
time2 = data.Date.values[ind][n:]
TKN2 = data.TKN.values[ind][n:].astype(float)
DON2 = np.zeros(len(data.DON[ind][n:]))
for i in range(len(data.DON[ind][n:])):
	try:
		DON2[i] = float(data.DON.values[ind][n+i])
	except:
		DON2[i] = 0
NH42 = TKN2 - DON2
NO32 = data.DissNitrateNitrite.values[ind][n:].astype(float)
PO42 = data.DissOrthoPhos.values[ind][n:].astype(float)

N = len(time1) + len(time2)
NH4 = np.zeros(N)
NO3 = np.zeros(N)
PO4 = np.zeros(N)

time = np.asarray(list(time1) + list(time2))

NH4[:len(time1)] = NH41
NH4[len(time1):] = NH42

NO3[:len(time1)] = NO31
NO3[len(time1):] = NO32

PO4[:len(time1)] = PO41
PO4[len(time1):] = PO42

sac_nut = pd.DataFrame({'Date':time, 'nh4': NH4, 'no3': NO3, 'po4': PO4})

time = pd.DataFrame(pd.date_range(start = '10/1/2016', end = '1/1/2018')) 
time.columns = ['time'] 
time.index = time.time 
time.columns = ['Date']

sac_df = pd.merge(time, sac_flow, how='left', on='Date')
sac_df = pd.merge(sac_df, sac_nut, how='left', on='Date')

sac_df.columns = ['Date', 'flow ft3/s', 'NH3 mg/L N', 'NO3 mg/L N', 'PO4 mg/L P']

false_sac_new = false_sac.append(sac_df, ignore_index=True)
false_sac_new.to_csv('../outputs/intermediate/false_sac.csv')

if 0:
	fig, ax = plt.subplots(nrows=4, sharex=True)

	ax[0].plot(false_sac_new['Date'], false_sac_new['flow ft3/s'], label='Flow')
	ax[0].legend(loc='best')
	ax[1].plot(false_sac_new['Date'][np.isfinite(false_sac_new['NH3 mg/L N'])], false_sac_new['NH3 mg/L N'][np.isfinite(false_sac_new['NH3 mg/L N'])], label='NH3')
	ax[1].legend(loc='best')
	ax[2].plot(false_sac_new['Date'][np.isfinite(false_sac_new['NO3 mg/L N'])], false_sac_new['NO3 mg/L N'][np.isfinite(false_sac_new['NO3 mg/L N'])], label='NO3')
	ax[2].legend(loc='best')
	ax[3].plot(false_sac_new['Date'][np.isfinite(false_sac_new['PO4 mg/L P'])], false_sac_new['PO4 mg/L P'][np.isfinite(false_sac_new['PO4 mg/L P'])], label='PO4')
	ax[3].legend(loc='best')


### use D26 for San Joaquin
s = 'D26'
ind = np.where(data.Station==s)[0]

time = data.Date.values[ind]
TKN = np.zeros(len(data.TKN[ind]))
for i in range(len(data.TKN[ind])):
	try:
		TKN[i] = float(data.TKN.values[ind][i])
	except:
		TKN[i] = 0
DON = np.zeros(len(data.DON[ind]))
for i in range(len(data.DON[ind])):
	try:
		DON[i] = float(data.DON.values[ind][i])
	except:
		DON[i] = 0
NH4 = TKN - DON
NO3 = data.DissNitrateNitrite.values[ind].astype(float)
PO4 = data.DissOrthoPhos.values[ind].astype(float)

sj_nut = pd.DataFrame({'Date':time, 'nh4': NH4, 'no3': NO3, 'po4': PO4})

time = pd.DataFrame(pd.date_range(start = '10/1/2016', end = '1/1/2018')) 
time.columns = ['time'] 
time.index = time.time 
time.columns = ['Date']

sj_df = pd.merge(time, sj_flow, how='left', on='Date')
sj_df = pd.merge(sj_df, sj_nut, how='left', on='Date')

sj_df.columns = ['Date', 'flow ft3/s', 'NH3 mg/L N', 'NO3 mg/L N', 'PO4 mg/L P']

false_sj_new = false_sj.append(sj_df, ignore_index=True)
false_sj_new.to_csv('../outputs/intermediate/false_sj.csv')








