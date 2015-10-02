import commands
import requests
from bs4 import BeautifulSoup as BS4
import csv
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

person_dict = {}
careers = ["0300", "0600", "1700", "4900", "1600", "4200", "1000", "1100", "1300", "1400", "1500", "3600", "1900", "3200", "2100", "3700", "0110", "2400", "2500", "0500", "2900", "3300", "8000", "0700", "3900", "4000", "1650", "4300", "2800", "2200", "4500", "4600", "4700", "4800", "5000", "5200"]
cookie_header = xxxxx # FILL THIS IN WHENEVER
# curl 'https://apps.carleton.edu/alumni/directory/?career_fields=0300' 
count = 0
for group in careers:
    html = commands.getoutput("curl ENTER THIS INFORMATION MANUALLY")
    soup = BS4(html)

    job_field = soup.title.get_text()[36:]

    for person in soup.find_all(attrs={"class":"person"}):
        print count
        count = count + 1

        name = ""
        year = ""
        major = ""
        email = ""
        phone = ""
        partner = ""
        address = ""
        work = ""
        education = ""
        status = ""
        facebook = ""
        linked_in = ""
        alumni_profile = ""
        
        nameLine = person.find(attrs={"class":"nameLine"})
        if nameLine != None:
            if nameLine.h3 != None:
                name = nameLine.h3.get_text()
            if nameLine.find(attrs={"class":"year"}) != None:
                year = nameLine.find(attrs={"class":"year"}).get_text()
            if nameLine.find(attrs={"class":"major"}) != None:
                major = nameLine.find(attrs={"class":"major"}).get_text()
                major = major[1:-1]

        personInfo = person.find(attrs={"class":"personInfo"})
        status = person.find(attrs={"class":"status"})
        if status != None:
            status = status.get_text()
            name = name + " (" + status + ")"
        else:
            if personInfo != None:
                infoGroup1 = personInfo.find(attrs={"class":"infoGroup group1"})
                if infoGroup1 != None:
                    if infoGroup1.a != None:
                        email_group = infoGroup1.a.find(attrs={"class":"email"})
                        if email_group != None:
                            email = email_group.get_text()
                    phone_potential = infoGroup1.find(attrs={"class":"phone"})
                    if phone_potential != None:
                        phone = phone_potential.get_text()
                    partner_potential = infoGroup1.find(attrs={"class":"partner"})
                    if partner_potential != None:
                        partner = partner_potential.get_text()
                infoGroup2 = personInfo.find(attrs={"class":"infoGroup group2"})
                if infoGroup2 != None:
                    address_potential = infoGroup2.find(attrs={"class":"address"})
                    if address_potential != None:
                        address = address_potential.get_text()
                    work_potential = infoGroup2.find(attrs={"class":"work"})
                    if work_potential != None:
                        work = work_potential.get_text()
                infoGroup3 = personInfo.find(attrs={"class":"infoGroup group3"})
                if infoGroup3 != None:
                    education_potential = infoGroup3.find(attrs={"class":"education"})
                    if education_potential != None:
                        education = education_potential.get_text()
                    econtacts = infoGroup3.find(attrs={"class":"econtacts"})
                    if econtacts != None:
                        for link in econtacts.li:
                            print "LINK!: " + str(link)
                            link_type = link.get_text()
                            if link_type == "Facebook":
                                facebook = link["href"]
                            elif link_type == "LinkedIn":
                                linked_in = link["href"]
                            elif link_type == "Alumni Profile":
                                alumni_profile = link["href"]
                          
        # print "PERSON!"
        # print name
        # print year
        # print major
        # print email
        # print phone
        # print partner
        # print address
        # print work
        # print education
        # print facebook
        # print linked_in
        # print alumni_profile

        person_stats = (name, year, major, email, phone, partner, address, work, education, job_field, facebook, linked_in, alumni_profile)

        if person_stats not in person_dict:
            person_dict[person_stats] = 1

csv_list = []
csv_list.append(["Name", "Year", "Major", "Job Field", "Work", "Education", "Email", "Phone", "Address", "Partner", "Facebook", "LinkedIn", "Alumni Profile"])
for index in person_dict:
    info_bloc = [index[0], index[1], index[2], index[9], index[7], index[8], index[3], index[4], index[6], index[5], index[10], index[11], index[12]]
    csv_list.append(info_bloc)

if len(csv_list) != 0:
    filename = "TEST_ALUMNI_DOWNLAOD"
    myfile = open(filename + "-unfinished.csv", 'wb')
    wr = csv.writer(myfile, dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL)
    wr.writerows(csv_list)
    myfile.close()

    open(filename + ".csv", "w").write("sep=,\n" + open(filename + "-unfinished.csv").read())
    os.remove(filename + "-unfinished.csv")
else:
    print "Failed to collect any information."

print "Done!"

















