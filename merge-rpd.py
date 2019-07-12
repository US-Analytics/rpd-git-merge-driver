#!/usr/bin/env python

""" 
US-Analytics 
RPD Merge Script

This script allows merges RPD files automatically. The variables at the top of this script must be updated.

The Git repository must include the .gitattributes file with the below body:
*.rpd merge=usa-obiee

Add the below content to the .gitconfig file (use 'git config --global --list --show-origin' to find it):
[merge "usa-obiee"]
	name = US-Analytics RPD merge driver.
	driver = merge-rpd.py %O %A %B

Examples of the above files are included in this repository.

"""

import time
import os 
import sys
from shutil import copyfile
from subprocess import Popen, PIPE, STDOUT, call
import subprocess
from glob import glob

# Input Parameters
rpd_password = "Password01"
admin_tool_exe = "C:\\Oracle\\OBIEEClient\\bi\\bitools\\bin\\admintool.cmd"
repository_path = "C:\\Users\Administrator\\Desktop\\rpd-devops-test\\"


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
		raise Exception("Error deleting file: "+str(e))

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
	command_body = "OpenOffline " + a_current + " " + password
	command_body += "\nMerge "+original+" "+b_modified+" decisions.csv "+password+" "+password+" "+output_name
	command_body += "\nSaveAs "+output_name
	command_body += "\nClose"
	command_body += "\nExit"
		
	# save args file
	write_file(command_file_name, command_body)
	
	#execute command
	command_string = [admin_tool_exe, "/Command", repository_path+command_file_name]
	p = Popen(command_string, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	errcode = p.returncode
	if errcode != 0:
		raise Exception("Merge failed: "+str(errcode))
		
# main method	
if __name__ == "__main__":
	try:
		if len(sys.argv) <= 1:
			raise Excepton("Not enough arguments.")
		action = sys.argv[1]
		
		# merge actions
		if action == "merge":
			# validate input
			if len(sys.argv) <= 3:
				raise Exception("Not enough arguments for merge.")
			original_rpd_path = sys.argv[1]
			current_rpd_path = sys.argv[2]
			modified_rpd_path = sys.argv[3]
			
			# some constants we need
			command_file_name = "commands.usa"
			rpd_extension = ".rpd"
			decisions_temp_file = "decisions.csv"
			
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
			print(sys.argv)
			exit()
			if len(sys.argv) <= 2:
				raise Exception("Not enough arguments for diff.");	
		else:
			raise Exception("No valid action found: '"+action+"'. Valid actions: (merge, diff)");
		exit(0)
	except Exception as e:
		print("Error - "+str(e))
		exit(1)
