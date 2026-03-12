from sys import exit
from time import sleep
from datetime import datetime
from glob import glob
from os import makedirs, path

# Big thanks to Christopher Koch 
#https://github.com/Kopachris/Epycor
from Epycor.client import ERP


def EpiAPICall(ServerRoot, InstanceName, APIKey, Company, Username, Password):
	ERPObj = ERP(ServerRoot, InstanceName, APIKey, Company)
	ERPObj.Login(Username, Password)
	print('\033[1A' + '\033[K', end='')
	print('Success! '+' '*30)
	
	# Session Logs
	QueryResults = ERPObj.Ice.BO.AdminSessionSvc.GetList(whereClause='',pageSize=0,absolutePage=1).json()['returnObj']
	
	ERPObj.Logout()
	return QueryResults 

def LogCurrentUse(LogDir,QueryResults):
	CountDict = {}	
	ListofAllCompanies = ['Total']
	
	for row in QueryResults['AdminSessionList']:
		if row['InUse'] == True:
				# Get All Company Usgae
			TotalSession = 'Total_'+row['SessionTypeDescription']
			CountDict[TotalSession] = CountDict.get(TotalSession, 0) + 1
				
				# Get Specific Company Usage
			CurCompSession = row['CurComp']+'_'+row['SessionTypeDescription']
			CountDict[CurCompSession] = CountDict.get(CurCompSession, 0) + 1
			
				# Hold these for later
			if row['CurComp'] not in ListofAllCompanies:
				ListofAllCompanies.append(row['CurComp'])
	
	# Fill out the results with zeros
	for SessionType in ['DataCollection','DefaultUser','EnterpriseProcessing']:
		for Company in ListofAllCompanies:
			CompSession = Company+'_'+SessionType
			if CompSession not in CountDict:
				CountDict[CompSession] = 0
	
	# Output the data
	MyDateTime = datetime.strftime(datetime.now(), '%m-%d-%Y %H-%M')
	OutFile = LogDir+MyDateTime+' Session Log.csv'
	with open(OutFile, 'w') as f:
		f.write('License Type,In Use,Allocation\n')
		for k in sorted(CountDict):
			v = CountDict[k]
			for Company in ListofAllCompanies:
				if Company in k:
					print(k,v)
					f.write(k+','+str(v)+',\n')
	
	return ListofAllCompanies

def AggregateData(LogDir,OutFile,ListofAllCompanies):
	# Build Summary Information
	DateCountDict = {}
	for file in glob(LogDir+'*Session Log.csv'):
		TimeStamp = datetime.strptime(file.replace(LogDir,''), '%m-%d-%Y %H-%M Session Log.csv')
		TimeStampStr = datetime.strftime(TimeStamp, '%m/%d/%Y %H:%M')
		DateCountDict[TimeStampStr] = {}
		with open(file, 'r') as f:
			lines = f.read().split('\n')
		if 'License Type' in lines[0]:
			del lines[0]
		for line in lines:
			if not line in ['','\n']:
				linelist = line.split(',')
				Type = linelist[0]
				Utilized = linelist[1]
				try:
					Allocation = linelist[2]
				except:
					Allocation = 0
				DateCountDict[TimeStampStr][Type] = {'Utilized':Utilized, 'Allocation':Allocation}
	
	ListofSessionTypes = ['DataCollection', 'DefaultUser','EnterpriseProcessing']
	
	# Output the Summary
	with open(OutFile, 'w') as f:
		f.write('TimeStamp,')
		for j in ListofSessionTypes:
			for i in ListofAllCompanies:
				Type = i+'_'+j
				f.write(Type+' Utilzed,')
		f.write('\n')
		
		for TimeStampStr, d in DateCountDict.items():
			f.write(TimeStampStr+',')
			for j in ListofSessionTypes:
				for i in ListofAllCompanies:
					Type = i+'_'+j
					f.write(str(d[Type]['Utilized'])+',')
			f.write('\n')

def PromptAPIKey():
	Password = input('Enter your API Key Password: ')
	print('\033[1A' + '\033[K', end='')
	print(' '*70)
	return Password
	
def PromptUserPass():
	Password = input('Enter your Epicor Password: ')
	print('\033[1A' + '\033[K', end='')
	print('Logging in... '+' '*30)
	return Password

if __name__ == '__main__':
	LogDir 			= 'Session Logs\\'
	OutFile			= 'Session Summary.csv' # Outputs to this files directory
	ServerRoot 		= 'MyBaseURL'
	InstanceName 	= 'MyInstanceName'
	APIKey 			= 'MyApiKey' #or APIKey = PromptAPIKey()
	Username 		= 'MyUsername'
	Company 		= 'AnyCompany'
	Password 		= PromptUserPass()
	
	# Build the Log Directory if needed
	if not path.isdir(LogDir):
		makedirs(LogDir)
	
	while True:
		QueryResults = EpiAPICall(ServerRoot, InstanceName, APIKey, Company, Username, Password)
		ListofAllCompanies = LogCurrentUse(LogDir,QueryResults)
		AggregateData(LogDir,OutFile,ListofAllCompanies)
		sleep(3600)
		