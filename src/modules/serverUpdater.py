# -*- coding: utf-8 -*-

import re
import subprocess


class serverUpdater( object ):

    def __init__( self ):

        pass


    def readconf( self ,conffile ):
        pass

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


    def updateFile( self ):
        pass



if __name__ == '__main__':

    su = serverUpdater( )
    ips = su.getIP()
    print ips
