class macTableParser( object ):


    def __init__( self , serverAddr , macTableList ,serverSN ):

        #self.serverMacList = self._getMacAddrList( serverAddr )
        #self.macPair = self._parser( self.serverMacList , macTableList )
        self.macPair = self._parser( serverAddr , macTableList ,serverSN )

    def _getMacAddrList( self, addr ):

        rr = []

        for key in addr.values():
            #print key
            rr.append( key )

        return rr


    def _macTranser( self , macAddr ):

        """
            input : f04d-a208-7b0e, f04d.a208.7b0e , f0:4d:a208:7b:0e,
            return mac  12 chars string like  12fd40af01d

        """

        address = ''
        try:
            if macAddr.find('.') != -1 :
                addr = macAddr.split( '.' )
            elif macAddr.find( '-' ) != -1:
                addr = macAddr.split( '-' )
            elif macAddr.find( ':' ) != -1 :
                addr = macAddr.split( ':' )
            for val in addr:
                address += val
        except :
            print 'addr is not mac address'

        return address.lower()



    def _parser( self , addrList , tableList ,serverSN ):

        state = False
        pairList = []

        for serverIP,serverMac in addrList.items() :
            for table in tableList:
                sw_ip = table['oob_ip']
                #print sw_ip
                rr = {}
                if len(table['data']) != 0:
                    for sw_mac,sw_port in table['data'][0].items() :
                        if self._macTranser(serverMac) == self._macTranser( sw_mac ):
                            #print 'same is ===> ' , serverMac , sw_mac , sw_port, sw_ip
                            rr['sw_ip'] = sw_ip
                            rr['server_ip'] = serverIP
                            rr['port'] = sw_port
                            rr['server_mac'] = serverMac
                            rr['SN'] = serverSN
                            state = True

                            pairList.append( rr )


        return pairList , state



