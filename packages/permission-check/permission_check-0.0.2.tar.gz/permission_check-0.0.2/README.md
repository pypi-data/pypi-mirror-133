# Permission Check
A simple, cross-platform, lightweight utility to check permission of files and folders in Python.

## Usage
1. `pip install permission-check`
2. `from permission_check.permission_check import PermissionCheck`
3. `file = PermissionCheck(path="path_to_your_file")` (A `FileNotFoundError` will occur if the path is not an existing file or folder on the file system)
### For checking Owner Permissions
#### Read
`if file.owner.has_read():`
    `print("Owner has read permissions"")`
#### Write
`if file.owner.has_write():`
    `print("Owner has write permissions"")`
#### Execute
`if file.owner.has_execute():`
    `print("Owner has execute permissions"")`

### For checking Group and Others user's Permissions
For checking Group and Other user's permissions just to `file.group` and `file.others` respectively. followed by the `.has_all()` or `.has_read()` or `.has_write()` or `.has_execute()` methods