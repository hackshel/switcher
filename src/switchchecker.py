import time
import os
import sys
import logging
import json
import re
import pprint

from os.path import basename
from urlparse import urlsplit
import urllib2

os.environ['LANGUAGE'] = 'en_US'
prefixdir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append( prefixdir+'/lib/python2.4/site-packages/' )
datadir = os.path.join( prefixdir+'/data')
sourceDir = os.path.join( prefixdir + '/sourceData' )
serverInfoData = sourceDir + '/serverinfo.txt'
switchData = sourceDir + '/switchs.txt'
switchconf = os.path.join(prefixdir+ '/conf' + '/switch.conf')

default_mutex_port = 10086


from modules import util
from modules import netutil
from modules import macTablePareser
from modules import poster
from modules import switchOEM
from modules import switchUpdater



def getSwitchDataByFile(  ):


    switchList  = util.getSwitchList( switchData )

    for switch in  switchList :
        if len( switch ) ==0 :
            pass
        else:
            addr = switch

        pairList = []
        for x in addr:
            swo = switchOEM.switchOEM( x ) # return switchOEM object ,name swo
            if swo.switchOEM == 'Cisco' :
                print x
                from modules import cisco
                sc = cisco.CiscoMacTableFileCreator( x )  # return  cisco switch object , sc is  mac table list
                result = sc.ret
            elif swo.switchOEM == 'H3C':
                pass
            elif swo.switchOEM == 'HuaWei':
                pass
            else:
                print '%s error , lost connect' % x


            if result != '':
                cstr  =  x + ' file is creat sussess !'
                #break
            else:
                cstr = x + ' file is null  '
            macFileCreator( result, x ,datadir )
            print cstr


    status = util.createFinishFlag( '__Finish__' , datadir ,str( time.time() ).split( '.' )[0] )

    print status



def getSwitchDataByCMDB( host ,port ):

    switchListObject = switchUpdater.switchUpdater( switchconf, host,port ) # return object of switch ip0

    addr =  switchListObject.data


    for x in addr:
        swo = switchOEM.switchOEM( x ) # return switchOEM object ,name swo
        if swo.switchOEM == 'Cisco' :
            from modules import cisco
            sc = cisco.CiscoMacTableFileCreator( x )  # return  cisco switch object , sc is  mac table list
            result =  sc.ret
        elif swo.switchOEM == 'H3C':
            from modules import cisco
            sc = cisco.CiscoMacTableFileCreator( x )  # return  cisco switch object , sc is  mac table list
            result = sc.ret
        elif swo.switchOEM == 'HuaWei':
            print x+'H3C'
            result = ''
        else:
            print '%s error , lost connect' % x

        if result != '':
            cstr  =  x + ' file is creat sussess !'
        else:
            cstr = x + ' file is null  '
        util.macFileCreator( result, x ,datadir )
        print cstr


    status = util.createFinishFlag( '__Finish__' , datadir ,str( time.time() ).split( '.' )[0] )

    return status

if __name__ == '__main__':


    #host = '10.210.128.199'
    host = '10.55.38.100'
    port = '9999'


    fileList = util.tarList( datadir )
    #util.download( 'http://10.88.15.156:8001/serverinfo.txt' , serverInfoData )
    (flag ,timer) = util.flag_checker( datadir, fileList ) # return timer used to up file or not
    print flag ,timer 
    #stime = int (str( time.time() ).split('.')[0] ) - int(timer[0])
    #print stime

    if flag != 'Finish' or flag == '' : # to update mac address list


        status = getSwitchDataByCMDB( host ,port )


    macTableList = []

    for file in fileList:
        if file != '__Finish__':

            macTableList.append(   util.macTableFileReader( datadir , file ) )

    #pprint.pprint (macTableList )


    serverInfoList = util.serverInfoLoader(  serverInfoData  )

    for serverInfo in serverInfoList:
        serverAddr = serverInfo['addr']
        serverSN   = serverInfo['SN']

        macAddrParse = macTablePareser.macTableParser(   serverAddr , macTableList ,serverSN )

        if macAddrParse.macPair[1] == True:
            MacPair =  macAddrParse.macPair[ 0 ]
            #print MacPair
            for pair in  MacPair:
                if pair != {} :
                    print pair
                    #p =  poster.poster( '10.210.128.199','9999' ,pair )
                    #p =  poster( '10.55.38.100','9999' ,pair )
                    #print p.stat


