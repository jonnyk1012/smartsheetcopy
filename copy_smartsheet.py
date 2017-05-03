import sys

DEFAULT_SOURCE_FOLDERID = 6248778823952260 #Template ID
DESTINATION_ID = 5403602073216900 # Folder ID fo 1.active projects Folder ID

def main(talkenid, name, sourcefolderid = DEFAULT_SOURCE_FOLDERID ): #Template ID
	import smartsheet

	SOURCE_FOLDER_NAME = 'Template'

	# Set a talken ID to get your Smartsheet API access
	print('Check Project Name, {0}'.format(name))

	smartsheet = smartsheet.Smartsheet(talkenid)

	# Get list of folders in "Sheets" folder.
	action = smartsheet.Folders.list_folders(DESTINATION_ID, include_all=True)

	try:
		folders = action.data
	except:
		print('Ooops! You should set a valid talken ID..{0}'.format(talkenid))
		exit()

	folders = action.data

	# Check a given folder name is not exist in the list
	i=0
        print('Total count {0}'.format(action.total_count))

	for i in range(action.total_count):

        	if folders[i].name == name:
                	print('{0} is already exist. Try other name'.format(name))
          		exit()
        	else:
                	i+=1


	# Check a given template_folderID is exist
	template_folderid = sourcefolderid # Default is Template folder ID
        #print('template_folderid is {0}'.format(template_folderid))


	if DEFAULT_SOURCE_FOLDERID == template_folderid:
		print('Source FolderID is {0}'.format(template_folderid))
	else :
        	i=0
                id_much = False
        	for i in range(action.total_count):
                	if folders[i].id == int(template_folderid) :
				id_much = True
				SOURCE_FOLDER_NAME = folders[i].name
				print('will copy from {0} folder, SOURCE_FOLDER_NAME is {1}'.format(folders[i].name,SOURCE_FOLDER_NAME))
			else:
                        	i+=1

		if bool(id_much) != True:
			print('Folder Id does not much what you specified .. {0}'.format(template_folderid))
			exit()

	# Copy a folder from the template folder.  Default ins Template folder ID
	action = smartsheet.Folders.copy_folder(
    	template_folderid, #Target folder to copy from : Template folder
    	smartsheet.models.ContainerDestination({
        	'destination_id': DESTINATION_ID, # If destination_type is home, then null
        	'destination_type': 'folder',
        	'new_name': name
    		}),
	include = 'all'
 	)

	folderId = action.result.id

	# Get sheets list. Specify the Folder Id
	action = smartsheet.Folders.get_folder(folderId)
	sheets = action.sheets

	#  Rename sheets name in the folder
	i=0
 	newname = name

	for i in range(len(sheets)):

        	orgname = sheets[i].name
        	dst = orgname.replace(SOURCE_FOLDER_NAME, newname)
        	action = smartsheet.Sheets.update_sheet(
        	sheets[i].id,
        	smartsheet.models.Sheet({
                	'name': dst ,
                	})
        	)

        	print('File name is modified as {0}'.format(dst))
        	i+=1


if __name__ == '__main__':
    args = sys.argv
 
    if len(args) == 3:
        talkenid = args[1]
        name     = args[2]
        main(talkenid, name)
    elif len(args) == 4:
	talkenid = args[1]
	name     = args[2]
	sourcefolderid = args[3]
	main(talkenid, name, sourcefolderid)
    else:
        print('Please sepcify with following format ')
        print('$ smartsheetcopy <Talken ID> <Project Name> [Option: <Source Folder ID>]')
        quit()

