# Secure Copy Plus #

SCP+ is a package of extensions for SCP, written in Python.
Additionally provides the following features:

  * validate transfer by MD5 hash comparison
  * continue interrupted transfers
  * tar folders and bzip2 files before transfer, unpack on the remote machine (not yet)

## Console Arguments ##

  * multiple sources: files or folders
  * one target: must be a folder