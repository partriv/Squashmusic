from django.utils.encoding import smart_str
from musicbar.util import exception_util

def getNodeText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    thes = ''.join(rc)
    try:
        #thes = thes.decode('latin-1').encode('utf-8')
        #thes = thes.decode('iso-8859-1').encode('utf-8')
        thes= smart_str(thes)        
    except:
        pass 
        #print "COULDNT DECODE THES", thes, exception_util.get_exception_str()
        #thes = thes.encode("ascii", "ignore")
        #print "SO THES"
    return thes

def getCData(node):
    nn = [n.data for n in node.childNodes if n.nodeType==node.CDATA_SECTION_NODE]
    if len(nn) > 0: 
        return nn[0]
    return ''