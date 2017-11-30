import json
import requests
'''
GLOBAL VARIABLES
'''
fileName = "cupid-dump.json"
everyUnitFromCupid = json.load(open(fileName,'r'))

newUnitArray = []
reqHeaders = {
  "Content-Type": "application/json"
}

def title_case(string):
  if string == 'OFFICE OF THE DVC (GLOBAL ENGAGEMENT)':
    return 'Office of the DVC (Global Engagement)'
  elif string != '':
    newString = string.split(' ')
    for i in range(len(newString)):
        newString[i] = newString[i][0].upper() + newString[i][1:].lower()
    return ' '.join(newString)
  else:
    return None

def convertOfferings(string):
  locations = {}
  if(string != ''):
    offerings = string.split('\n\n')
    for i in range(len(offerings)):
      currentOffering = (offerings[i].split(': '))
      location = currentOffering[1].split(' ')
      campus = location[0]
      classType = location[1]

      tp = currentOffering[0].split(' ')
      year = (tp[0])
      semester = ' '.join(tp[1:])
      fullCode = year+"-"+semester
      try:
        if(classType == "ON-CAMPUS2017"):
          classType = "ON-CAMPUS"
        locations[campus][fullCode].append(classType) 
      except:
        if(classType == "ON-CAMPUS2017"):
          classType = "ON-CAMPUS"
        locations[campus] = {}
        locations[campus][fullCode] = [classType]

    return locations
  else:
    return None


for unit in everyUnitFromCupid:
  u = {}


  u['unitCode'] = unit['Unit code']
  u['unitName'] = unit['Title']
  u['faculty'] = title_case(unit['Owning faculty'])
  u['unitLevel'] = unit['Unit level']
  u['teachingPeriods'] = convertOfferings(unit["Offering details (Future years only)"] + unit["Offering details (Current year only)"])
 
  
  u['preqs'] = unit['Prerequisites']
  u['coreqs'] = unit['Corequisites']
  u['proh'] = unit['Prohibitions']

  u['descrip'] = ' '.join(unit['Handbook synopsis'].split())
  

  u['creditPoints'] = unit['Credit points']
  u['scaBand'] = int(unit['Highest SCA band'])
  u['eftsl'] = unit['Unit EFTSL']
  
  u['levelType'] = unit["Undergraduate, Postgraduate or Both"]
  u['unitObjectives'] = unit["Unit objectives"]
  u['relevantAOS'] = unit["Unit objectives"]


  u['studyLoad'] = unit["Workload requirements"]
  u['assessment'] = unit["Assessment"]
  r = requests.post("https://monplan-api-au-dev.appspot.com/api/units", data=json.dumps(u), headers=reqHeaders)
  print(r.status_code, r.reason)


print(json.dumps(newUnitArray, indent=4, sort_keys=True))