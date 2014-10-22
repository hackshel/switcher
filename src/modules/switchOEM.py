import util

"""
Base Class of the Switch snmp class

"""

class switchOEM( object ):

    def __init__( self, ip ):

        self.community_string  = 'bdHH&xbS'
        self.oid = 'sysDescr'
        self.switchIP = ip
        self.switchOEM = self.get_sysDescr( self.community_string , self.switchIP , self.oid )

    def get_sysDescr( self,  key, ip, oid ):

        dev = util.shellcmd(  "snmpwalk -v 2c -c '%s' %s  %s" % (key,ip,oid) ).split('\n')
        if dev[0].find( 'Cisco') != -1 :
            oem  = 'Cisco'
        elif dev[0].find('H3C') !=-1 :
            oem = 'H3C'
        else:
            oem = 'Other'

        return oem


