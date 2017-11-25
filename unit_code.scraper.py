from lxml import html
import requests
import json

class Scraper:
  year = 2017
  baseURL = "https://monash.edu/pubs/" + str(year) + "handbooks"
  units = []

  def getUnits(self):
    posA = ord('a')
    posZ = ord('z')
    for i in range(posA, posZ+1):
      targetURL = self.baseURL + "/units/index-bycode-" + chr(i) + ".html"
      page = requests.get(targetURL)
      tree = html.fromstring(page.content)
      for unit in tree.xpath('//*[@class="hbk-index-list hbk-index-list__units hbk-index-list__units__codes"]/li'):
        unitCode = unit.text_content().split(" ")[0]
        print(unitCode)
        if(unitCode != None):
          self.units.append(unitCode)

class UnitScraper:
  year = 2017
  baseURL = "https://monash.edu/pubs/" + str(year) + "handbooks"

  def __init__(self, unitCode):
    self.unitCode = unitCode
    self.page = requests.get(self.baseURL + "/units/" + unitCode + ".html")
    self.pageTree = html.fromstring(self.page.content)

  def getUnitDescription(self):
    description = self.pageTree.xpath('//*[@id="content_container_"]/div[3]')[0].text_content().split()
    return " ".join(description)

  def getUnitTeachingPeriod(self):
    teachingPeriodObject = {}
    teachingPeriods = self.pageTree.xpath('//*[@id="preamble-' + self.unitCode +'"]/div/*')[2:]
    for i in range(0, len(teachingPeriods), 2):
      location = teachingPeriods[i].text_content()
      nested_text = teachingPeriods[i+1]
      teachingPeriodArray = nested_text.text_content().replace(")", ") ").split()
      semesters = []
      for i in range(0, len(teachingPeriodArray), 4):
        semString = " ".join(teachingPeriodArray[i : i+4])
        semesters.append(semString)
      teachingPeriodObject[location] = semesters
    return teachingPeriodObject

  def getPreqs(self):
    preqs = self.pageTree.xpath('//*[@id="content_container_"]/div[9]')[0].text_content().split()
    return " ".join(preqs)

  def getProh(self):
    preqs = self.pageTree.xpath('//*[@id="content_container_"]/div[10]')[0].text_content().split()
    return " ".join(preqs)

  def getProh(self):
    preqs = self.pageTree.xpath('//*[@id="content_container_"]/div[11]')[0].text_content().split()
    return " ".join(preqs)

S = Scraper()
US = UnitScraper('FIT1049')
parsed = json.loads(json.dumps(US.getPreqs()))
print(json.dumps(parsed, indent=4, sort_keys=True))
