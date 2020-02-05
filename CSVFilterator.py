
import argparse
import csv

import json
import yaml
import re


print ("""                           
                    _:*///:_                     
                _+*///////////+_                
    ____----*////////////////////**----____    
   *//////////////////////////////////********    
   */////////////////       ////**************    
   *////////////////          /***************    
   *///////////////   /////   ****************    
   *//////////////   /////**   ***************    
   *//////////////   ////***   ***************    
   *//////////////   ///****   ***************    
   *////////////                 *************    
   *////////////    Saleh Bin    *************    
   *////////////     Muhaysin    *************    
   *////////////                 *************    
    *////////********************************     
     */////  github.com/salehmuhaysin  *****      
      *///*********************************             
==========================================================""")

# return json in a beautifier
def json_beautifier(js):
    return json.dumps(js, indent=4, sort_keys=True)

class CSVFilterator:

	columns = []
	rules = None
	def __init__(self, csvFile , filterFile, outFile , delimiter):
		
		print( "[+] Input CSV file: " 	+ csvFile )
		print( "[+] Filter rules: " 	+ filterFile) 
		print( "[+] Output file: " 		+ outFile )

		self.matches = {}
		self.get_rules(filterFile)
		print("[+] Rules: ")
		for r in self.rules:
			self.matches[r] = 0
			print("[+]\t\t" + r)

		with open(outFile , 'w') as fout:
			with open(csvFile) as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				line_count = 0
				filtered_lines = 0
				blacklisted_lines = 0
				total_lines = 0
				for row in csv_reader:

					# write first row
					if line_count == 0:

						columns = row
						fout.write('"' + delimiter.join(row) + '"\r\n' )
						line_count += 1 
					# check other rows
					else:
						total_lines +=1
						# if the line blacklisted then include it 
						if self.include_line( columns , row):
							# write the line to output file
							fout.write('"' + delimiter.join(row) + '"\r\n' )
							blacklisted_lines += 1
							line_count += 1 
							continue
						
						# if line should be filtered, skip the line
						if self.filter_line( columns, row):
							filtered_lines += 1 # counter for the number of skipped lines
							continue 

						# write the line to output file
						fout.write('"' + delimiter.join(row) + '"\r\n' )
						line_count += 1

				# print the filtered information
				print("[+] Total lines \t\t["+str(total_lines)+"]")
				print("[+] Total lines returned \t["+str(line_count-1)+"]")
				print("[+] Number of lines Filtered \t["+str(filtered_lines)+"]")
				print("[+] Number of lines Blacklisted ["+str(blacklisted_lines)+"]")

				print("[+] Blacklisted rules: ")
				for r in self.rules:
					if self.rules[r]['_type'] == 'blacklist':
						print("[+] Matches ["+str(self.matches[r])+"] > " + r)
				print("[+] Whitelisted rules:")
				for r in self.rules:
					if self.rules[r]['_type'] == 'whitelist':
						print("[+] Matches ["+str(self.matches[r])+"] > " + r)


			fout.close()

	# get the list of rules from the yaml file
	def get_rules(self , file):
		with open(file) as f:
			self.rules = yaml.load(f)

	# check if the value matches the condition terms
	def match_values(self, value, condition , matches , case_sensitive = True):
		if type(matches) != list:
			matches = [matches]

		for m in matches:
			m = str(m)

			# if case sensitive
			if not case_sensitive:
				m = m.lower()
				value = value.lower()

			if condition == '=':
				if m == value:
					return True
			elif condition == '~':
				if m in value:
					return True
			elif condition == '^':
				if value.startswith(m):
					return True
			elif condition == "$":
				if value.endswith(m):
					return True
			elif condition == 'r':
				if re.search(m , value):
					return True

		return False


	# return True then include the line on the output result
	def include_line(self , columns , line):
		fields = dict(zip(columns, line))

		for rule in self.rules:
			# if the rule type is not blacklisting the line, skip it
			if self.rules[rule]['_type'] != "blacklist":
				continue


			isMatch = True
			for col in self.rules[rule]:
				# if the yaml field start with "_" then dont consider it as a column name
				if col.startswith("_"):
					continue


				case_sensitive = True 
				if '_case_sensitive' in self.rules[rule][col].keys() and self.rules[rule][col]['_case_sensitive'] == False:
					case_sensitive = False

				match = self.match_values(fields[col] , self.rules[rule][col]['condition'] , self.rules[rule][col]['values'] , case_sensitive=case_sensitive)

				if not match:
					isMatch = False
					break

			if isMatch:
				self.matches[rule] += 1
				return True

		return False


	# return True then filter the line
	def filter_line(self , columns, line):
		# combine columes and line into one dictionary
		fields = dict(zip(columns, line))

		# for each rule, check if it is match the line or not, if match then filter it
		for rule in self.rules:
			# if the rule type is not whitelisting the line, then skip the rule
			if self.rules[rule]["_type"] != 'whitelist':
				continue



			isMatch = True
			for col in self.rules[rule]:
				# if the yaml field start with "_" then dont consider it as a column name
				if col.startswith("_"):
					continue

				case_sensitive = True 
				if '_case_sensitive' in self.rules[rule][col].keys() and self.rules[rule][col]['_case_sensitive'] == False:
					case_sensitive = False

				match = self.match_values(fields[col] , self.rules[rule][col]['condition'] , self.rules[rule][col]['values'] , case_sensitive=case_sensitive)

				if not match:
					isMatch = False
					break

			if isMatch:
				self.matches[rule] += 1
				return True

		return False


def main():
	# ================== arguments
	a_parser = argparse.ArgumentParser('Python script tool filter CSV files based on predefined ruleset')
	
	requiredargs = a_parser.add_argument_group('required arguments')
	requiredargs.add_argument('-i', dest='filter', help='filter file contain YAML filter rule', required=True)
	requiredargs.add_argument('-f', dest='csvfile', help='CSV file to be filtered', required=True)
	a_parser.add_argument('-o' , dest='out_file' , help='Output csv file (default: <csvfile>-filtered.csv)')
	a_parser.add_argument('-d' , dest='delimiter' , help='Output CSV file delimiter (default ",")')
	args = a_parser.parse_args()

	out_file 	= args.csvfile.rstrip('.csv') + "-filtered.csv"
	delimiter 	= ','

	if args.out_file != None:
		out_file = args.out_file

	
	if args.delimiter != None:
		delimiter = args.delimiter

	delimiter = '"' + delimiter + '"'

	f = CSVFilterator(args.csvfile , args.filter , out_file , delimiter)


main()