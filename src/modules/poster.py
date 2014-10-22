import os
import pprint
import httplib
import json


class poster( object  ):

    def __init__( self, host,port,dic ):

        self.switchAn = self.getSNByIP0( host , port ,dic['sw_ip'] )

        if self.switchAn == '':
            self.stat = 'switch %s is not in the CMDB' % dic['sw_ip']
        else:

            self.serverMac,self.serverID = self.getServerBySN( host,port , dic['SN'] )
            self.postData, self.state = self.postDataFormater( self.switchAn ,self.serverMac , self.serverID, dic )

            if  self.state == True:
                self.stat = self.do_post( host,port ,self.postData )
            else:
                self.stat =  'Error: mac addr not match. %s' % self.postData

    def getSNByIP0( self, host, port , ip ):

        conn = httplib.HTTPConnection( host,port )

        url = '/search?q=ip0==' + ip
        conn.request( 'GET', url )
        res = conn.getresponse()

        an = ''

        if res.status == 200 :
            rs = eval(res.read())
            try:

                if len( rs['result'] ) != '':
                    rr = rs['result'][0]
                    if  rr != {} and rr['ip0'] == ip:

                        an =  rr['asset_number']

            except IndexError:
                #print 'switch is not in the CMDB'
                pass

        return an


    def getServerBySN( self , host , port ,sn):


        conn = httplib.HTTPConnection( host,port )

        url = '/search?q=sn==' + sn
        conn.request( 'GET', url )
        res = conn.getresponse()

        serverMac = {}
        serverid = ''
        if res.status == 200 :

            rs = eval(res.read())

            try:
                if len( rs['result'] ) != '':

                    rr = rs['result'][0]

                    if  rr != {} and rr['sn'] == sn:
                        serverMac['mac0'] = rr['mac0']
                        serverMac['mac1'] = rr['mac1']
                        serverMac['mac2'] = rr['mac2']
                        serverMac['mac3'] = rr['mac3']
                        serverid = rr['.id']
            except IndexError:
                print sn+ "is  not at cmdb "

        return serverMac ,serverid

    def postDataFormater( self , switchAn, serverMac , serverid , d ):


        pdata = {}

        d['switch_an'] = switchAn
        d['serverid']  = serverid

        try:
            for key , value in serverMac.items() :
                #print key , value
                if value == d['server_mac']:
                    d['sw_no'] = key
                    break
                else:
                    d['sw_no'] = 'Error'

            if d['sw_no'] == 'mac0':
                switch_no = 'switch0'
            elif d['sw_no'] == 'mac1':
                switch_no = 'switch1'
            elif d['sw_no'] == 'mac2':
                switch_no = 'switch2'
            elif d['sw_no'] == 'mac3' :
                switch_no = 'switch3'
            elif d['sw_no'] == 'Error' :
                switch_no = 'Error NO'


        except KeyError:
            pass

        if d['serverid'] != '' and switch_no != 'Error NO' :
            pdata['id'] = d['serverid']
            pdata['value'] = {}
            pdata['value'][switch_no] = d['switch_an'] +'#' +d['sw_ip']+ '#' + d['port']

            return pdata ,True

        else:

            return  d , False


    def do_post( self , host, port, data ):

        result = ''
        data['manifest'] = 'rack_server'

        #print data
        conn = httplib.HTTPConnection( host,port )
        url = '/node/%s' % ( data['id'] )
        conn.request( 'POST', url ,json.dumps(data) )
        res = conn.getresponse()


        #res.read()
        #print res.reason

        if res.status == 200 :

            r = res.read()
            if r != '':

                rr = json.loads( r )
                if rr['success'] == True:
                    result =   'Update data %s , %s'  % ( data , res.reason )

        return result



