# rpd-git-merge-driver
A Git Merge Driver for the RPD.

Provided through the MIT License. Refer to LICENSE.

# Description

A custom Git merge driver to merge binary RPD files. The script configures Git to offload the merge reponsibilities to the Administration Tool when working with files that have a '.rpd' extension. The merge process is the same as you see happen inside the Administration Tool. In fact, Git will open the Administration Tool itself and provide all required values (except in the case of a merge conflict).

# Installation instructions

1. Ensure Python3 is installed and available on the PATH (execute 'python -V').
2. Move the 'merge-rpd.py' script to a location on the machine. Record the path.
3. Open the 'merge-rpd.py' script using the editor of your choice, and update lines 30, 31, and 32.
4. These variables should be set to the RPD password, the path to the Admin Tool executable, and the path to the RPD Git repository (not this repository), respectively.
5. Ensure all Windows paths are represented using '\\' instead of '\'. Save and close the script.
6. Add the 'merge-rpd.py' script to the PATH environment variable.
7. Copy the contents of the provided '.gitattributes' file to the '.gitattributes' file in the RPD Git repository (not this repository). 
8. If this file does not exist, copy the provided '.gitattributes' file to the RPD Git repository. Confirm the file is '.gitattributes' and not '.gitattributes.txt'.
8. Add, Commit, and Push the RPD Git repository to persist this file. This file must be present in order for the merge script to work correctly.
9. Find the location of the local '.gitconfig' file using the command: 'git config --global --list --show-origin'
10. Open the '.gitconfig' file and append the contents of the provided '.gitconfig' file. Save the file.
11. The changes in step 10 must be made on every machine that will perform an RPD merge.
12. Any open Powershell/CMD sessions must be restarted for the changes to take effect.


# Requirements

* Python3 (Python2 is unsupported).
* Windows OS supported by the Administration Tool.
* Oracle Administration Tool.
* Git 2.0.0+
