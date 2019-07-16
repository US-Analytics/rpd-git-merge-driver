#!/usr/bin/env python

""" 
US-Analytics 
RPD Merge Script

This script allows merges  and diffs of RPD files automatically. The variables at the top of this script must be updated.

The Git repository must include the .gitattributes file with the below body:
*.rpd merge=usa-obiee-merge
*.rpd diff=usa-obiee-diff

Add the below content to the .gitconfig file (use 'git config --global --list --show-origin' to find it):
[merge "usa-obiee"]
        name = US-Analytics RPD merge driver.
        driver = merge-rpd.py merge %O %A %B
[merge "usa-obiee-merge"]
        name = US-Analytics RPD merge driver.
        driver = merge-rpd.py merge %O %A %B
[diff "usa-obiee-diff"]
        name = US-Analytics RPD diff driver.
        command = merge-rpd.py diff
[difftool "usa-obiee-diff"]
        name = US-Analytics RPD diff driver.
        cmd = merge-rpd.py diff

Examples of the above files are included in this repository.

"""

import time
import os 
import sys
from shutil import copyfile
from subprocess import Popen, PIPE, STDOUT, call
import subprocess
from glob import glob
import csv

# Input Parameters
rpd_password = "Password01"
admin_tool_exe = "C:\\Oracle\\OBIEEClient\\bi\\bitools\\bin\\admintool.cmd"


# save a file with the body of contents to a file named filename
def write_file(filename, contents):
	try:
		f = open(filename, "w")
		f.write(contents)
		f.close()
	except Exception as e:
		raise Exception("Error writing to file: "+str(e))

			
# delete a file from the file system			
def delete_file(f):
	try:
		if type(f) is not str:
			f.close()
			f = f.name
		if os.path.exists(f):
			os.remove(f)
	except Exception as e:
		#raise Exception("Error deleting file: "+str(e))
		pass


# copy a file from the orig location to the dest location (optionally delete original)
def copy_file(orig, dest, delete=False):
	try:
		for f in glob(orig):
			copyfile(f, dest)
			if delete:
				delete_file(f)
	except Exception as e:
		raise Exception("Error copying file: "+str(e))

			
# perform the three way merge for the RPD		
def three_way_merge(original, a_current, b_modified, output_name, password, command_file_name):
	try:
		command_body = "OpenOffline " + a_current + " " + password
		command_body += "\nMerge "+original+" "+b_modified+" decisions.csv "+password+" "+password+" "+output_name
		command_body += "\nSaveAs "+output_name
		command_body += "\nClose"
		command_body += "\nExit"
			
		# save args file
		write_file(command_file_name, command_body)
		
		# execute
		execute_rpd_commands(command_file_name)
	except Exception as e:
		raise Exception("Merge RPD failed: "+str(e))


# perform comparison of RPD files
def compare_rpd(current_file, other_file, output_file, password, command_file_name):
	try:
		command_body = "Hide"
		command_body += "\nOpenOffline "+current_file + " " + password
		command_body += "\nCompare "+other_file+ " " + password + " " + output_file
		command_body += "\nClose"
		command_body += "\nExit"
	
		# save args file
		write_file(command_file_name, command_body)
			
		# execute
		execute_rpd_commands(command_file_name)
	except Exception as e:
		raise Exception("Compare RPD failed: "+str(e))


# execute an rpd command
def execute_rpd_commands(command_file_name):
	command_string = [admin_tool_exe, "/Command", command_file_name]
	p = Popen(command_string, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	errcode = p.returncode
	if errcode != 0:
		raise Exception("Command failed: "+str(errcode))


# main method	
if __name__ == "__main__":
	try:
		if len(sys.argv) <= 1:
			raise Exception("Not enough arguments.")
		action = sys.argv[1]
		
		# merge actions
		if action == "merge":
			# validate input
			if len(sys.argv) <= 5:
				raise Exception("Not enough arguments for merge.")
			original_rpd_path = sys.argv[2]
			current_rpd_path = sys.argv[3]
			modified_rpd_path = sys.argv[4]
			repository_path = os.getcwd()
			
			# some constants we need
			command_file_name = repository_path+os.path.sep+"commands.usa"
			rpd_extension = ".rpd"
			decisions_temp_file = repository_path+os.path.sep+"decisions.csv"
			
			# files must have the .rpd extension, so we add it
			copy_file(original_rpd_path, original_rpd_path+rpd_extension, True)
			copy_file(current_rpd_path, current_rpd_path+rpd_extension, True)
			copy_file(modified_rpd_path, modified_rpd_path+rpd_extension, True)
	
			# decisions file must not be empty
			write_file(decisions_temp_file, "Decision\n")
			
			# perform the merge
			three_way_merge(original_rpd_path+rpd_extension, current_rpd_path+rpd_extension, modified_rpd_path+rpd_extension, current_rpd_path, rpd_password, command_file_name)
			
			# delete all the temp files we created
			delete_file(current_rpd_path+rpd_extension)
			delete_file(modified_rpd_path+rpd_extension)
			delete_file(original_rpd_path+rpd_extension)
			delete_file(command_file_name)
			delete_file(decisions_temp_file)
		elif action == "diff":
			# diff actions
			# validate inputs
			if len(sys.argv) <= 7:
				raise Exception("Not enough arguments for diff.");	
			my_file = sys.argv[2]
			first_file = sys.argv[3]
			second_file = sys.argv[6]
			repository_path = os.getcwd()
			
			# constants we need
			output_file_path = repository_path+os.path.sep+"comparison_output.csv"
			command_file_name = repository_path+os.path.sep+"commands.usa"
			
			# execute the compareRPD using the two files, saving as a CSV file
			compare_rpd(second_file, first_file, output_file_path, rpd_password, command_file_name)
			
			# parse the output file
			output_string = ""
			with open(output_file_path, "r") as csv_file:
				reader = csv.reader(csv_file)
				output_string += "diff --git a/"+my_file+" b/"+my_file
				output_string += "\n@@ -1, 1 @@"
				for row in reader:
					item_name = str(row[0])
					item_change = str(row[1])
					item_type = str(row[2])
					item_location = str(row[3])
					item_change_icon = "+"
					if item_change == "Deleted":
						item_change_icon = "-"
					output_string+="\n"+item_change_icon + " ("+item_change+") "+item_type+ " with name "+item_name+" in "+item_location+" layer."
			
			# clean up
			delete_file(command_file_name)
			delete_file(output_file_path)
			print(output_string)
		else:
			raise Exception("No valid action found: '"+action+"'. Valid actions: (merge, diff)");
		
		# exit with success code
		exit(0)
	except Exception as e:
		print("Error - "+str(e))
		exit(1)
