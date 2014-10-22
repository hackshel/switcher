
import subprocess
import os
import subprocess


from os.path import basename
from urlparse import urlsplit
import urllib2
import httplib
import time 


# TODO rmeove these

class ShellError( Exception ): pass
class ShellCommandError( ShellError ): pass

def shellcmd( cmd ):
    return os.popen( cmd ).read()

def shell_call( *args ):

    subproc = subprocess.Popen(
            args,
            close_fds = True,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
    )

    out, err = subproc.communicate()

    subproc.wait()

    rc = subproc.returncode
    return [ rc, out, err ]





def tarList( path ):

    r = {}
    tarfiles = os.listdir( path )

    return tarfiles





def serverInfoLoader(  file ):

    rr = []
    fp = open( file , 'r' )
    o = fp.xreadlines()

    for r in o :
        ds  = eval(   r.split('\n')[0]  )
        rr.append( ds )

    return rr




"""
mac table file reader , open mac table file ,and read lines into list.
read and load the mac addr table file into memorary
"""
def macTableFileReader( path, tableFile ):

    macTable = {}
    macTableData = []

    macTable['oob_ip'] = tableFile

    fp =  open( path+'/'+tableFile , 'r' )
    c = fp.readlines()
    for line in c :
        (filepath,filename) = os.path.split( fp.name )
        ds = eval (line)
        if len( ds ) == 0:
            pass
        else:

            rr = {}
            for r in ds:
                for key,val in r.items():
                    rr[val] = key 
            macTableData.append( rr )


    macTable['data'] = macTableData

    return macTable


def flag_checker( datadir, fileList ):

    flag = ''
    ctime = ''

    for file in fileList:
        if  file.startswith( '__' ):
            fp =  open( datadir +'/' + file )
            name =  fp.name.split( '/' )[-1]
            ctimer = fp.readlines()
            fp.close()

            flag = name.split( '__' )[1]
            ctime = timer[0].split( '\n')

            break

        else:
            ctime = str(time.time()).split('.')[0]
    return   flag , time



def createFinishFlag( flag ,path, timestmp ):

    try:
        fp = open( path+'/'+flag , 'w' )
    except IOError:
        return False
    fp.write( timestmp )
    fp.close()
    return True

"""
    read switch list file and change file to list
"""
def getSwitchList ( f ):

    with open( f ) as fp:
        lines = fp.xreadlines()
        for line in lines :
            line = line.split( '\n' )[0]
            ips = line.split( ' '  )
            yield ips



def macFileCreator( data, filename , dataDir ):

    fp = open( dataDir+'/'+filename , 'w')
    if data != '' :
        fp.write( str(data) )
    else:
        fp.write( '' )
    fp.close()

def timeChecker( fileTime ):
    pass


def url2name(url):
    return basename(urlsplit(url)[2])

def download(url, localfilename = None):
    localname = url2name(url)
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)

    if r.info().has_key('content-disposition'):
        # if the response has content-disposition, we take file name from it
        localname = r.info()['content-disposition'].split('filename=')[1]
        if localname[0] == '"' or localname[0] == "'":
            localname = localname[1:-1]
    elif r.url != url:
        # if we were redirected, the real file name we take from the final url
        localname = url2name(r.url)
    if localfilename:
        # we can force to save the file as specified name
        localname = localfilename
    f = open(localname, 'wb')
    f.write(r.read())
    f.close()




