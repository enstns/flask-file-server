import os
from flask import Flask, render_template, request
from flask import send_from_directory

MAIN_DIRECTORY = 'C:\\Users\\enestanas\\Desktop\\flask-file-server\\' # dont forget last "\\" 
DEBUG = True

app = Flask(__name__)
app.config['password'] = "12345" # to control user when try to change main directory

def show_files(folder):
    return (os.listdir(MAIN_DIRECTORY + folder))

# http://127.0.0.1:4000/
@app.route("/")
def main():
    return {
        "ERROR_STATUS" : False,
        "Message" : "Wellcome flask-file-server...",
        "SERVER-URLS" : {
            "to_list_files" : {
                "URL": "http://127.0.0.1:4000/filelist",
                "PARAMETERS": {
                    "folder" : "to list different folder's files which is in main directory (not necessary if wants to list maindirectory)"
                },
                "BODY" :None,
                "TEST_URL" : [
                    "http://127.0.0.1:4000/filelist",
                    "http://127.0.0.1:4000/filelist?folder=files"
                ]
            },
            "to_open_file" : {
                "URL": "http://127.0.0.1:4000/openfile",
                "PARAMETERS": {
                    "file_name" : "the selected file name which is wanted to open...",
                    "folder_path" : "to define where is selected file is located (not necessary if file in main directory)"
                },
                "BODY" :None,
                "TEST_URL" : [
                    "http://127.0.0.1:4000/openfile?file_name=13.png&folder_path=files\test2",
                    "http://127.0.0.1:4000/openfile?file_name=phoca-download-r.png&folder_path=files" 
                ]
            },
            "to_update_maindirectory" : {
                "URL": "http://127.0.0.1:4000/update/maindirectory",
                "PARAMETERS": None,
                "BODY" : {
                    "password" : "server password to change directory!",
                    "new_directory" : "new main directory.."
                }
            }
        }
    }

# example GET request
# http://127.0.0.1:4000/filelist
# http://127.0.0.1:4000/filelist?folder=files
@app.route("/filelist",methods=['GET'])
def list_files():
    if request.method == 'GET':
        folder = request.args.get('folder')
        if folder!=None:
            if len(folder.split(".")) == 1: 
                try:
                    files=show_files(folder)
                except Exception as e:
                    return  {
                        'ERROR_STATUS' : True,
                        'REASON' : str(e)
                    }
                else:
                    files_json = {}
                    count = 0
                    for file in files:
                        files_json[count] = file
                        count+=1
                    return  files_json
        else:
            files=show_files("")
            files_json = {}
            count = 0
            for file in files:
                files_json[count] = file
                count+=1
            return  files_json
    return  {
            'ERROR_STATUS' : True,
            "REASON" : "Bad request",
            "URL" : "Request URL must be like that : /filelist",
            "PARAMETERS" : {
                "folder" : "use this parameter if try to get file list in different folder where in DOWNLOAD_FOLDER.Otherwise unnecessary parameters."
                }
            }

# example GET request
# http://127.0.0.1:4000/openfile?file_name=13.png&folder_path=files\test2
# http://127.0.0.1:4000/openfile?file_name=phoca-download-r.png&folder_path=files
@app.route('/openfile', methods=['GET'])
def open_file():
    if request.method == 'GET':
        file = request.args.get('file_name')
        if file != None:
            folder = request.args.get('folder_path')
            try:
                if folder != None:
                    return send_from_directory(MAIN_DIRECTORY+folder, file)
                else:
                    return send_from_directory(MAIN_DIRECTORY , file)
            except Exception as e:
                if folder != None:
                    return {
                        "ERROR_STATUS" : True,
                        "REASON" : "Cannot open file: " + MAIN_DIRECTORY + str(folder) + "\\" +str(file)
                    }
                else:
                    return {
                        "ERROR_STATUS" : True,
                        "REASON" : "Cannot open file: " + MAIN_DIRECTORY+str(file)
                    }
    return {
        "ERROR_STATUS" : True,
        "REASON" : "Bad request",
        "URL" : "Request URL must be like that : /openfile",
        "PARAMETERS" : {
            "file_name" : "selected file name to open (must be defined)",
            "folder_path" : "use this parameter if try to open file which is in different folder in DOWNLOAD_FOLDER.Otherwise unnecessary parameters."
        }
    }

# example POST request
# URL: http://127.0.0.1:4000/update/maindirectory
# BODY:  
# {
#     "password" : "12345",
#     "new_directory" : "C:\\Users\\admin\\Desktop\\"
# }
@app.route('/update/maindirectory', methods=['POST'])
def update_maindirectory():
    global MAIN_DIRECTORY
    if request.method == 'POST':
        try:
            message = request.get_json()
        except Exception as e:
            return {
                    "ERROR_STATUS" : True,
                    "REASON" : str(e),
                }
        else:
            if message != None:
                try:
                    password = message["password"]
                    if password == app.config["password"]:
                        old_folder = MAIN_DIRECTORY
                        MAIN_DIRECTORY = message["new_directory"]
                        return {
                                "ERROR_STATUS" : False,
                                "OLD_DIRECTORY" : old_folder,
                                "NEW_DIRECTORY" : MAIN_DIRECTORY
                            }
                    else:
                        return {
                                "ERROR_STATUS" : True,
                                "REASON" : "Unauthorized update directory request!"
                        }
                except Exception as e:
                    pass
    return {
        "ERROR_STATUS" : True,
        "REASON" : "Bad URL",
        "URL" : "Request URL must be like that : /update/maindirectory",
        "REQUEST_BODY" : {
            "password" : "12345",
            "new_directory" : "C:\\Users\\admin\\Desktop"
        }
    }

if __name__ == "__main__":
    app.secret_key = "Tahir-Sultan"
    app.run(debug=False,host='0.0.0.0', port=4000)