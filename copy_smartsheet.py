import sys
import argparse
import os

DEFAULT_SOURCE_FOLDERID = 6248778823952260 #Template ID
TEMPLATE_FCB_ID = 4025456254052228 # Template for FCB ID
DESTINATION_ID = 5403602073216900 # Folder ID fo 1.active projects Folder ID
TALKEN_ID_PATH = '~/talkenid.txt' #File of Talked id 

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

	for i in range(action.total_count):

        	if folders[i].name == name:
                	print('{0} is already exist. Try other name'.format(name))
          		exit()
        	else:
                	i+=1


	# Check a given template_folderID is exist
        if sourcefolderid == 'FCB':
                template_folderid = TEMPLATE_FCB_ID
        else :
		template_folderid = sourcefolderid # Default is Template folder ID
        #print('template_folderid is {0}'.format(template_folderid))


	if DEFAULT_SOURCE_FOLDERID == template_folderid:
                action = smartsheet.Folders.get_folder(template_folderid)
                print('Source FolderID is {0}'.format(action.name))
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

        	#print('File name is modified as {0}'.format(dst))
        	i+=1


if __name__ == '__main__':
	args = sys.argv

        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--id', dest='talkenid', required=False,
                                help='set your talked Id of smartsheet')
        parser.add_argument('-o', '--output', dest='project_name', required=True,
                                help='set your project name')
        parser.add_argument('-s', '--source', dest='template_folder', required=False,
                                default= DEFAULT_SOURCE_FOLDERID,
                                help='set a folder id of smartsheet or "FCB" ')

	args = parser.parse_args()

        if args.talkenid != None:
                main(args.talkenid, args.project_name, args.template_folder)
        else:
                f = open(os.path.expanduser("/home/junk/talkenid.txt"),'r')
                print("file contents-1",f.readline())
                f.close()

                print TALKEN_ID_PATH
                m = open(os.path.expanduser(TALKEN_ID_PATH),'r')
                print("file contents-2")
                talkenid = m.readline()[:-1]  # Take rid of '\n' by [:-1]
                #main(talkenid, args.project_name, args.template_folder)
                print ("file contents-3",talkenid)
                m.close()


                if os.path.isfile(os.path.expanduser(TALKEN_ID_PATH)) == True:  # Open the file(talkenid.txt) to get talkenid
                        f = open(os.path.expanduser(TALKEN_ID_PATH),'r')
                        talkenid = f.readline()[:-1]  # Take rid of '\n' by [:-1]
                        main(talkenid, args.project_name, args.template_folder)
                        f.close()
                else: # If there is no file for Talken id, need to specify talken id as argument
                        print('Specify talken ID by -i or --id')

	quit()

