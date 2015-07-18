previous versions were working, but currently it doesn't ...

contributors welcome!

## scp space bug ##
  * spaces in paths are recognized in the first source, but not in the target argument
  * must be escaped in target, must not be escaped in source
  * workaround included in [scp.py](http://code.google.com/p/md5-merge-directories/source/browse/trunk/scp.py)