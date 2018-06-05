#!/usr/bin/env python3

"""
parse.py

Noah Kaufman wrote this script.
Lwin Moe modified it and made it into a manage.py command. Instead of this, we should now run:
   python3 manage.py import_vcards URL
The issue with this script is that Django wouldn't allow `exec` because of security risks.
The script will still run as a stand-alone program from the command line.
   python3 parse.py
"""


import vobject
import geocoder
import requests
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "geoling.settings"
import django
django.setup()
from geoevent.models import Contact, Adr, Adr_type, Email, Email_type, Tel, Tel_type, Label, Role, URL, Org, Nickname


#file = "geoling_vcards.vcf"
#with open(file, "r") as f:
#    data = f.read().split("END:VCARD")   #"_".join(f.read().split("-")).split("END:VCARD")

# TODO:
# set your CardDAV URL, login and password here:
r = requests.get("URL",auth=('LOGIN','PASSWD'))
r.encoding = "utf-8"
data = r.text.split("END:VCARD")
data.pop(-1)


type1 = ['adr']
type2 = ['email','tel']
type3 = ['label','nickname','role','url']
type4 = ['org']
type5 = ['fburl','fn','kind','n','prodid','uid','version','x-ablabel','x-abuid','x-evolution-assistant','x-evolution-blog-url','x-evolution-file-as','x-evolution-manager','x-evolution-spouse','x-evolution-video-url','x-evolution-webdav-href','x-linguistlist-editingstatus','x-linguistlist-editorapproval','x-linguistlist-institutionid','x-linguistlist-progalternatename','x-linguistlist-progappdeadline','x-linguistlist-progdescr','x-linguistlist-progdistinctions','x-linguistlist-progeditorcomment','x-linguistlist-progfinancialaid','x-linguistlist-programmid','x-linguistlist-progsize','x-linguistlist-progspecial','x-linguistlist-progstatus','x-linguistlist-progtitle','x-mozilla-html','x-radicale-name']


for vcard in data:
    #print(vcard)
    vcard += "END:VCARD"
    card = vobject.readOne(vcard)
    card_uid = card.uid.value
    #check to see if contact already exists
    try:
        contact = Contact.objects.get(uid=card_uid)
        print("Contact information already exists for: "+card.fn.value)
        Contact.objects.filter(uid=card_uid).delete()
    except Contact.DoesNotExist:
        print("creating contact for "+str(card.fn.value))
    except Contact.MultipleObjectsReturned:
        print("Found multiple objects for "+str(card.fn.value))
        continue

    c = Contact()
    c.save()
    #different fields need to be dealt with in different ways
    for field in card.contents:

        values = card.contents[field]
        for value in values:

            typ = 5 #default 5, only needs to check first 4 types then

            for i in range(1,5):
                exec("if field in type%d: typ=%d"%(i,i))

            if typ == 1: #address
                a = Adr(contact=c)
                a.save()
                a.post_office_box = card.adr.value.box
                a.extended_address = card.adr.value.extended
                a.street_address = card.adr.value.street
                a.locality = card.adr.value.city
                a.region = card.adr.value.region
                a.postal_code = card.adr.value.code
                a.country_name = card.adr.value.country
                a.type = card.adr.type_param

                coords = geocoder.google("%s %s,%s,%s %s"%(a.street_address, a.locality,a.region,a.country_name,a.postal_code))
                a.lon = coords.lng
                a.lat = coords.lat

                s_value = str(value)
                if s_value[3:5] != "{}":
                    params = s_value.split("[")[1].split("]")[0].split(",")
                    for param in params:
                        exec("typ = %s(%s=a,type=%s)" % (field[0].upper() + field[1:] + "_type", field, param.strip()))
                        typ.save()
                a.save()


            elif typ == 2: # email,telephone
                exec("et = %s(contact=c)"%(field[0].upper()+field[1:])) #create email or telephone object
                et.save()
                et.value = value.value    #add insert value
                s_value = str(value)       #turn into string for parsing
                if s_value[4:6] != "{}" and s_value[6:8] != "{}":  #get the paramaters
                    params = s_value.split("[")[1].split("]")[0].split(",")
                    for param in params:    #and then create an instance of that parameter
                        exec("typ = %s(%s=et,type=%s)" % (field[0].upper()+field[1:]+"_type",field,param.strip()))
                        typ.save()
                et.save()

            elif typ == 3: # label, nickname, role, url
                if field == "url": string = "%s = %s(contact=c)"%(field[0], field.upper())
                else: string = "%s = %s(contact=c)"%(field[0], field[0].upper()+field[1:])
                exec(string)
                exec("%s.data=value.value"%field[0]) #example: l.data = value
                exec("%s.save()" % field[0])

            elif typ == 4: # org
                o = Org(contact=c)
                o.organization_name = value.value[0]
                o.organization_unit = value.value[1]
                o.save()

            elif typ == 5: # everthing else
                exec("c.%s=value.value"%"_".join(field.split("-"))) #example: c.x_linguislist_xxxxx = value[0].value

    c.save()



    #exit()
    """
    adr

    email

    label

    nickname

    org

    role

    tel

    url


    fburl
    fn
    kind
    n
    prodid
    uid
    version


    x-ablabel
    x-abuid
    x-evolution-assistant
    x-evolution-blog-url
    x-evolution-file-as
    x-evolution-manager
    x-evolution-spouse
    x-evolution-video-url
    x-evolution-webdav-href
    x-linguistlist-editingstatus
    x-linguistlist-editorapproval
    x-linguistlist-institutionid
    x-linguistlist-progalternatename
    x-linguistlist-progappdeadline
    x-linguistlist-progdescr
    x-linguistlist-progdistinctions
    x-linguistlist-progeditorcomment
    x-linguistlist-progfinancialaid
    x-linguistlist-programmid
    x-linguistlist-progsize
    x-linguistlist-progspecial
    x-linguistlist-progstatus
    x-linguistlist-progtitle
    x-mozilla-html
    x-radicale-name


    """
    """
    #for field in card.contents:
    if len(card.contents) > 39:
        for i in sorted(card.contents):
            print("'"+'_'.join(i.split("-"))+"'") # + " = models.CharField(max_length=2000)")
        exit()
    """
    """
    if len(card.contents) > 39:
        for i in sorted(card.contents):
            print('_'.join(i.split("-"))) + " = models.CharField(max_length=2000)")
        exit()
"""

    """
    #print(card, "\n\n\n\n")
    #print("card\n\n"); card.prettyPrint()

    """
