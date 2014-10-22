# -*- coding: utf-8 -*-

import re
import subprocess
import ConfigParser
import httplib
import urllib
import json
import pprint

class switchUpdater( object ):

    def __init__( self , switch_conf , host, port):


        self.localIPs = self.getIP()
        if self.localIPs == []:
            print 'no local ips ,exit'
            sys.exit(1)
        self.conf = self.readconf( switch_conf )
        self.location = self.getLocationName( self.conf , self.localIPs )
        if self.location == '':
            print 'DEG Server not in switch.conf file,please check! '
            sys.exit(1)

        self.switchs = self.getSwitchListByCMDB( host,port , self.location )

        self.data = self.updateSwitchList( self.switchs ,host,port )


    def readconf( self ,conffile ):

        """读取配置文件"""
        config = ConfigParser.ConfigParser()
        config.read(conffile)
        sectionlist = config.sections()

        locationDict = dict(config.items( sectionlist[0] ))

        return locationDict

    def getIP( self ):

        """获取本机内外网ip,去除回环地址
        XXX: only for linux because dev only eth"""
        ipRe = re.compile("\s*inet\s*addr:([\d]*\.[\d]*\.[\d]*\.[\d]*)")
        p = subprocess.Popen('/sbin/ifconfig', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.communicate()[0]
        if p.returncode == 0:
            #addrlist = [ipRe.search(i).groups()[0] for i in filter(lambda x: x.startswith('eth'), result.split('\n\n'))]

            tmp = [ x for x in result.split('\n\n') if x.startswith('eth') ]
            tmp = [ ipRe.search(x) for x in tmp ]
            addrlist = [ x.groups()[0] for x in tmp if x ]

            return addrlist
        else:
            return []

    def getLocationName( self, locationDict ,localIPs ):

        r = ''
        for ip ,location  in locationDict.items():
            if ip in localIPs :
                r = location
        return r

    def getSwitchListByCMDB( self , host, port, location ):

        conn = httplib.HTTPConnection( host,port )
        url = '/search?num=0&q=manifest==switch' + urllib.quote(' and ') + 'rack~' + urllib.quote( location )
        conn.request( 'GET' , url )

        res = conn.getresponse()

        if res.status == 200:
            r = json.loads( res.read() )['result']

        return r

    def getSwitchIPByCMDB( self ,host,port, an ):

        conn = httplib.HTTPConnection( host,port )
        url = '/search?num=0&q=manifest==ip_info' + urllib.quote(' and ') + 'server_asset_number==' + urllib.quote( an )
        conn.request( 'GET' , url )

        res = conn.getresponse()

        if res.status == 200:
            r = json.loads( res.read() )['result']

        return r



    def updateSwitchList( self ,data ,host,port):

        ips = []
        for switch in data:
            if switch['ip0'] != '0.0.0.0' and switch['model'].startswith('F5') == False and switch['ip0'] != '':
                ips.append( switch['ip0'] )
            else:
                ip = self.getSwitchIPByCMDB( host, port,switch['asset_number'] )
                if( ip != [] ):
                    ips.append( ip[0]['ip_name'] )
        return ips


if __name__ == '__main__':

    switch_conf = '../conf/switch.conf'

    su = switchUpdater( )
    ips = su.getIP()
    conf = su.readconf( switch_conf )
    location = su.getLocationName( conf ,ips)
    sws = su.getSwitchListByCMDB( '10.55.38.100', '9999',location )
    data = su.updateSwitchList( sws )
