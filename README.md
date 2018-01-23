# smartsheetcopy
This is a utility tool of smartsheet
Copy folder and sheets/reports in the folder from template folder or you can specifed a desired folder

Activate API function:
You need to activate API function in your smartsheet account. 
http://smartsheet-platform.github.io/api-docs/#direct-api-access

CLI:
smartsheetcopy -o PROJECT_NAME -i TALKENID [-s TEMPLATE_FOLDER] 

Note:
If you create ~/snap/smartsheetcopy/common/talkenid.txt and discribe your talkenid in taleknid.txt,
you can omit -i TALKENID 
SmartSheet API 2.0 does not support to copy reports. You need to modify file name manually. 
