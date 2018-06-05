import vobject
import geocoder
import requests
from geoevent.models import Contact, Adr, Org, Adr_type, Email, Email_type, Tel, Tel_type, Label, Role, URL, Nickname

type1 = ['adr']
type2 = ['email','tel']
type3 = ['label','nickname','role','url']
type4 = ['org']
type5 = ['fburl','fn','kind','n','prodid','uid','version','x-ablabel','x-abuid','x-evolution-assistant','x-evolution-blog-url','x-evolution-file-as','x-evolution-manager','x-evolution-spouse','x-evolution-video-url','x-evolution-webdav-href','x-linguistlist-editingstatus','x-linguistlist-editorapproval','x-linguistlist-institutionid','x-linguistlist-progalternatename','x-linguistlist-progappdeadline','x-linguistlist-progdescr','x-linguistlist-progdistinctions','x-linguistlist-progeditorcomment','x-linguistlist-progfinancialaid','x-linguistlist-programmid','x-linguistlist-progsize','x-linguistlist-progspecial','x-linguistlist-progstatus','x-linguistlist-progtitle','x-mozilla-html','x-radicale-name']

def parseVcard(feed, user, passwd):
    #file = "geoling_vcards.vcf"
    #with open(file, "r") as f:
    #    data = f.read().split("END:VCARD")   #"_".join(f.read().split("-")).split("END:VCARD")

    r = requests.get(feed,auth=(user, passwd))
    r.encoding = "utf-8"
    data = r.text.split("END:VCARD")
    data.pop(-1)

    for vcard in data:
        # print(vcard)
        vcard += "END:VCARD"
        card = vobject.readOne(vcard)
        card_uid = card.uid.value
        # check to see if contact already exists
        try:
            contact = Contact.objects.get(uid=card_uid)
            print("Contact information already exists for: " + card.fn.value)
            Contact.objects.filter(uid=card_uid).delete()
        except Contact.DoesNotExist:
            print("creating contact for " + str(card.fn.value))
        except Contact.MultipleObjectsReturned:
            print("Found multiple objects for " + str(card.fn.value))
            continue
        c = Contact()
        c.save()
        # different fields need to be dealt with in different ways
        for field in card.contents:
            values = card.contents[field]
            for value in values:
                if field in type1:
                    typ = 1
                elif field in type2:
                    typ = 2
                elif field in type3:
                    typ = 3
                elif field in type4:
                    typ = 4
                else:
                    typ = 5 # TODO: this is no longer used. Can be removed.

                if typ == 1:  # address
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

                    coords = geocoder.google("%s %s,%s,%s %s" % (a.street_address, a.locality, a.region, a.country_name, a.postal_code))
                    a.lon = coords.lng
                    a.lat = coords.lat

                    s_value = str(value)
                    if s_value[3:5] != "{}":
                        params = s_value.split("[")[1].split("]")[0].split(",")
                        for param in params:
                            addr_type = param.strip().replace('\'', '')
                            typ = Adr_type(adr=a, type=addr_type)
                            typ.save()
                    a.save()

                elif typ == 2:  # email,telephone
                    if field == 'tel':
                        et = Tel(contact=c)
                        et.save()
                    elif field == 'email':
                        et = Email(contact=c)
                        et.save()

                    et.value = value.value  # add insert value

                    s_value = str(value)  # turn into string for parsing
                    if s_value[4:6] != "{}" and s_value[6:8] != "{}":  # get the paramaters
                        # and then create instances of the parameters
                        params = s_value.split("[")[1].split("]")[0].split(",")
                        for param in params:
                            addr_type = param.strip().replace('\'', '')
                            if field == 'tel':
                                typ = Tel_type(tel=et, type=addr_type)
                                typ.save()
                            if field == 'email':
                                typ = Email_type(email=et, type=addr_type)
                                typ.save()

                    et.save()

                elif typ == 3:  # label, nickname, role, url
                    if field == "url":
                        #string = "%s = %s(contact=c)" % (field[0], field.upper())
                        u = URL(contact=c)
                        u.data = value.value
                        u.save()
                    if field == 'role':
                        r = Role(contact=c)
                        r.data = value.value
                        r.save()
                    if field == 'label':
                        l = Label(contact=c)
                        l.data = value.value
                        l.save()
                    if field == 'nickname':
                        n = Nickname(contact=c)
                        n.data = value.value
                        n.save()

                elif typ == 4:  # org
                    o = Org(contact=c)
                    o.organization_name = value.value[0]
                    o.organization_unit = value.value[1]
                    o.save()

                # other fields
                if field == 'fburl':
                    c.fburl = value.value
                if field == 'fn':
                    c.fn = value.value
                if field == 'kind':
                    c.kind = value.value
                if field == 'n':
                    c.n = value.value
                if field == 'prodid':
                    c.prodid = value.value
                if field == 'uid':
                    c.uid = value.value
                if field == 'version':
                    c.version = value.value
                if field == 'x-ablabel':
                    c.x_ablabel = value.value
                if field == 'x-abuid':
                    c.x_abuid = value.value
                if field == 'x-evolution-assistant':
                    c.x_evolution_assistant = value.value
                if field == 'x-evolution-blog-url':
                    c.x_evolution_blog_url = value.value
                if field == 'x-evolution-file-as':
                    c.x_evolution_file_as = value.value
                if field == 'x-evolution-manager':
                    c.x_evolution_manager = value.value
                if field == 'x-evolution-spouse':
                    c.x_evolution_spouse = value.value
                if field == 'x-evolution-video-url':
                    c.x_evolution_video_url = value.value
                if field == 'x-evolution-webdav-href':
                    c.x_evolution_webdav_href = value.value
                if field == 'x-linguistlist-editingstatus':
                    c.x_linguistlist_editingstatus = value.value
                if field == 'x-linguistlist-editorapproval':
                    c.x_linguistlist_editorapproval = value.value
                if field == 'x-linguistlist-institutionid':
                    c.x_linguistlist_institutionid = value.value
                if field == 'x-linguistlist-progalternatename':
                    c.x_linguistlist_progalternatename = value.value
                if field == 'x-linguistlist-progappdeadline':
                    c.x_linguistlist_progappdeadline = value.value
                if field == 'x-linguistlist-progdescr':
                    c.x_linguistlist_progdescr = value.value
                if field == 'x-linguistlist-progdistinctions':
                    c.x_linguistlist_progdistinctions = value.value
                if field == 'x-linguistlist-progeditorcomment':
                    c.x_linguistlist_progeditorcomment = value.value
                if field == 'x-linguistlist-progfinancialaid':
                    c.x_linguistlist_progfinancialaid = value.value
                if field == 'x-linguistlist-programmid':
                    c.x_linguistlist_programmid = value.value
                if field == 'x-linguistlist-progsize':
                    c.x_linguistlist_progsize = value.value
                if field == 'x-linguistlist-progspecial':
                    c.x_linguistlist_progspecial = value.value
                if field == 'x-linguistlist-progstatus':
                    c.x_linguistlist_progstatus = value.value
                if field == 'x-linguistlist-progtitle':
                    c.x_linguistlist_progtitle = value.value
                if field == 'x-mozilla-html':
                    c.x_mozilla_html = value.value
                if field == 'x-radicale-name':
                    c.x_radicale_name = value.value
        c.save()
