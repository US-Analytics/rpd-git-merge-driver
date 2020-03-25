# rpd-git-merge-driver
Git Merge and Diff Drivers for the RPD developed by US-Analytics.

Provided through the MIT License. Refer to LICENSE.

# Description

A custom Git merge and diff driver to merge binary RPD files. The script configures Git to offload the merge and diff reponsibilities to the Administration Tool when working with files that have a '.rpd' extension. The merge process is the same as you see happen inside the Administration Tool. In fact, Git will open the Administration Tool itself and provide all required values (except in the case of a merge conflict). The diff process uses the Compare RPD functionality present in the Administration Tool (it does not use the comparerpd.bat script).

# Installation instructions

1. Ensure Python3 is installed and available on the PATH (execute 'python -V' to verify).
2. Move the 'merge-rpd.py' script to a location on the machine. Make sure the script has permissions to write files in this location.
3. Open the 'merge-rpd.py' script using the editor of your choice, and update lines 43, 44, and 45.
4. These variables should be set to the RPD password, the path to the Admin Tool executable, and a boolean flag (True or False) to log debug messages, respectively.
5. Ensure all Windows paths are represented using '\\\\' instead of '\\'. Save and close the script.
6. Add the 'merge-rpd.py' script to the PATH environment variable. This can be done by adding the containing folder to the PATH environment variable. Ensure it can be called from the command line via "merge-rpd.py". 
7. Copy the contents of the provided '.gitattributes' file to the '.gitattributes' file in the RPD Git repository (not this repository).
8. If this file does not exist, copy the provided '.gitattributes' file to the RPD Git repository. Confirm the file is '.gitattributes' and not '.gitattributes.txt'.
9. Add, Commit, and Push the RPD Git repository to persist the .gitattributes file. The file must be present in order for the merge and diff commands to work correctly.
10. Find the location of the local '.gitconfig' file using the command: 'git config --global --list --show-origin'
11. Open the '.gitconfig' file and append the contents of the provided '.gitconfig' file. Save the file.
12. The changes in steps 10 and 11 must be made on every machine that will perform an RPD merge.
13. Any open Powershell/CMD or Git GUI sessions must be restarted for the changes to take effect.


# Requirements

* Python3 (Python2 is unsupported).
* Windows OS supported by the Administration Tool.
* Oracle Administration Tool.
* Git 2.0.0+
