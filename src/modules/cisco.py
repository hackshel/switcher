import time
import os
import sys
import logging
import json
import netutil
import util
import re
import pprint


os.environ['LANGUAGE'] = 'en_US'
prefixdir = os.path.dirname(os.path.abspath(sys.argv[0]))
default_mutex_port = 10086
sys.path.append( prefixdir+'/lib/python2.4/site-packages/' )
datadir = os.path.join( prefixdir+'/data')



class CiscoMacTableFileCreator( object ):

    """
    use to create mac address Table File in data dictionary.
    The File Format like This:
    mac address  vlan  ports
    ------

    10bf.203f.aa0a  333 po10

    file name used switch ip address

    """

    def __init__( self  , ip) :

        self.switchIP = ip
        self.community_string  = 'bdHH&xbS'
        self.ifIndexOID = '.1.3.6.1.2.1.17.4.3.1.2'
        self.ifNameOID  = '.1.3.6.1.2.1.31.1.1.1.1'
        self.ciscoVlanOID = '.1.3.6.1.4.1.9.9.46.1.3.1.1.2'
        self.ciscoMacTableOID = '.1.3.6.1.2.1.17.4.3.1.1'
        self.ciscoPortStatOID = '.1.3.6.1.4.1.9.9.46.1.6.1.1.14'

        # do function 
        self.ret = self.process( self.switchIP , self.community_string )

    def getVlans( self, ip , key ,oid ):

        vlan = []
        try:
            dev = util.shellcmd(  "snmpwalk -v 2c -c '%s' %s  %s" % (key,ip,oid) ).split('\n')
        except:
            print 'Error vlan struct'

        for r in dev :
            r = r.split('=')[0]
            v =  r.split('.')[-1]
            if v != '' and int(v) < 1000:
                vlan.append( v.strip() )
        return vlan


    def getPortifName( self, ip,key,oid ,portIndex):

        pair = {}
        dev = util.shellcmd(  "snmpwalk -v 2c -c '%s' %s  %s" % (key,ip,oid) ).split('\n')
        for r in dev:
            if r != '':
                k = r.split('=')[0].split('.')[-1].strip()
                v = r.split('=')[1].split(':')[1].strip()
                for pi in portIndex:
                    if pi == k:
                        pair[pi] = v
        return pair


    def getPortIndex( self, ip,key,oid):

        port = []
        dev = util.shellcmd(  "snmpwalk -v 2c -c '%s' %s  %s" % (key,ip,oid) ).split('\n')
        for r in dev:
            if r != '' and r.find( 'INTEGER:') != -1 :
                k = r.split('=')[0].split('.')[-1].strip()
                v = r.split('=')[1].split(':')[1].strip()
                if int(v) != 1 and int(k) > 10000 :
                    port.append( k )
        return port

    def get_macTableByVlan( self, ip , key ,oid ,vlan ):

        dr = {}
        dev = util.shellcmd(  "snmpwalk -v 2c -c '%s'@%s %s  %s" % (key,vlan,ip,oid) ).split('\n')
        #pprint.pprint (dev)
        for r in dev:
            if r != '' and r.find('Hex-STRING:') != -1:
                k  = r.split('=')[0].strip()
                m =  r.split('=')[1].split(':')[1].strip()
                mac = m.replace(' ', ':')
                s =  k.split('.')[-6:]
                str  = '.'.join( s )

                dr[str] = mac

        return dr



    def get_ifIndexByVlan( self, ip, key,oid,vlan ):

        dr = {}
        dev = util.shellcmd(  "snmpwalk -v 2c -c '%s'@%s %s  %s" % (key,vlan,ip,oid) ).split('\n')
        #pprint.pprint( dev )
        for index in dev:
            if index != '' and index.find('INTEGER') != -1:
                k = index.split( '=' )[0].strip()
                r = index.split( '=' )[1].split(':')[1].strip()

                if r != '128'  and int(r) < 48 :
                    s =  k.split('.')[-6:]
                    str  = '.'.join( s )

                    dr[str] = r

        values=set()
        for kk in dr.keys():
            val = dr[kk]
            if val in values:
                del dr[kk]
            else:
                values.add(val)


        return dr


    def macToPortNumPair( self, index , macTable ,PortIndex):

        ret = {}
        if len(index) != 0 :
            for k,v in index.items():
                if macTable.has_key( k ):
                #print 'prot:'+v + ',mac addr:' + macTable[k]
                    if int(v) < 10:
                        v = '1010' + v
                    else:
                        v = '101' +v
                    for kk,vv in PortIndex.items():
                        if v == kk:
                            ret[vv] = macTable[k]
        return ret


    def process ( self ,ip ,community_string ):

        result = []
        vlan = self.getVlans( ip, community_string, self.ciscoVlanOID )
        portIndex = self.getPortIndex( ip , community_string , self.ciscoPortStatOID )
        portifName = self.getPortifName(  ip , community_string , self.ifNameOID ,portIndex )
        for v in vlan:
            ifIndex = self.get_ifIndexByVlan( ip,community_string,self.ifIndexOID,v )
            vlanMacTable = self.get_macTableByVlan( ip , community_string,self.ciscoMacTableOID, v)
            pair = self.macToPortNumPair( ifIndex , vlanMacTable ,portifName )
            if len(pair) != 0 :
                result.append( pair )

        return result
