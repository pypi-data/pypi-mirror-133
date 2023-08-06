import json
import os

checkFile = os.path.isfile('./data.json')

if checkFile == False:
  aDict = {"testUser":"Test Password"}
  jsonString = json.dumps(aDict)
  jsonFile = open("data.json", "a+")
  jsonFile.write(jsonString)
  jsonFile.close()


def auth():

  json_file = open("data.json")
  datafile = json.load(json_file)

  print('Please Enter your Username: ')
  userInput = input('')
  print('Please Enter your Password: ')
  passInput = input('')

  try:
    mainPass = datafile[userInput]

    if passInput == mainPass:
      print('Logged In!')

  except:
    print('User Not Found: Error 404')
    quit()



def register():

  print('Please Create your Username: ')
  userInput = input('')
  print('Please Create your Password: ')
  passInput = input('')

  a_dictionary = {userInput : passInput}

  with open("data.json", "r+") as file:
    data = json.load(file)
    data.update(a_dictionary)
    file.seek(0)
    json.dump(data, file)