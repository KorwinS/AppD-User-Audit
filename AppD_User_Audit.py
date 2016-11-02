import requests
from datetime import datetime, timedelta
import json
import csv
import xlsxwriter

def main(env):
	days = 7
	user_names = {}

	while days >= 0:
		# Set Time range vars
		start_date = datetime.now().date()-timedelta(days=days)
		end_date = datetime.now().date()-timedelta(days=days-1)
		start_time = str(start_date)+'T00:00:00.000-0000\\'
		end_time = str(end_date)+'T00:00:00.000-0000'

		# Query Controller for data
		if env == 'prod':
			url = "https://<INSERT APPD PROD URL>/controller/ControllerAuditHistory"
			headers = {
			    'authorization': "Basic <INSERT KEY HERE>",
			    'cache-control': "no-cache",
			    }
		elif env == 'test':
			url = "https://<INSERT APPD TEST URL>/controller/ControllerAuditHistory"
			headers = {
			    'authorization': "Basic <INSERT KEY HERE>",
			    'cache-control': "no-cache",
			    }
		else:
			print("OOOOOONOOOOOOOO")

		querystring = {"startTime":start_time,"endTime":end_time}
		response = requests.request("GET", url, headers=headers, params=querystring)

		# Turn query into something we can use
		json_dict = json.loads(response.text)

		# Loop through response, pulling out only Login actions
		x=0
		for i in json_dict:
			if 'LOGIN' in json_dict[x].get('action'):
				if '<INSERT API USERNAME HERE>' in json_dict[x].get('userName'):
					pass
				else:
					u_name = json_dict[x].get('userName')
					login_date = json_dict[x].get('auditDateTime')
					login_date_chopped = len(login_date.split()[-1])-10
					user_names.update({u_name:[login_date[:-login_date_chopped]]})
			x=x+1

		# Deincrement days var
		days = days - 1

	# Setup Excel Workbook, mess with formatting, etc
	workbook = xlsxwriter.Workbook('<INSERT PATH>/user_audit_'+env+'.xlsx')
	worksheet = workbook.add_worksheet()
	format1 = workbook.add_format({'bold': True, 'font_color': 'black', 'font_size': '14', 'bg_color':'99CCFF'})
	format2 = workbook.add_format({'bold': True, 'font_color': 'black', 'font_size': '14'})
	worksheet.set_column(0,1,14.2)
	worksheet.write('A1','Environment:',format1)
	worksheet.write('B1', env.upper(),format1)
	worksheet.write('A2','Username',format2)
	worksheet.write('B2','Login Date',format2)
	row = 1
	col = 0
	# Loop through the dict for usernames and write rows
	for key in user_names.keys():
	    row += 1
	    worksheet.write(row, col,     key)
	    for item in user_names[key]:
	        worksheet.write(row, col + 1, item)
	        row += 0

	# Close the workbook        
	workbook.close()

# Do the thing
if __name__ == '__main__':
	main('prod')
	main('test')