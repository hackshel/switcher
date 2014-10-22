import re

def ip_classification( ip ):
    # TODO deprecated

    intraPatterns = [ '172\..*',
                      '10\.[^.]*[13579]\..*',

                    ]

    for ptn in intraPatterns:

        if re.match( ptn, ip ):
            return 'intra'

    else:
        return 'extra'


def filter_ip_extra( ips ):
    # TODO deprecated
    return [ x for x in ips if ip_classification( x ) == 'extra' ]

def filter_ip_intra( ips ):
    # TODO deprecated
    return [ x for x in ips if ip_classification( x ) == 'intra' ]


