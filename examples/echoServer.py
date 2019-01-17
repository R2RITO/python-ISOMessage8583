"""

(C) Copyright 2009 Igor V. Custodio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import InvalidIso8583
import socket

# Configure the server
serverIP = "localhost"
serverPort = 8583
maxConn = 5
bigEndian = True
# bigEndian = False


# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind it to the server port
s.bind((serverIP, serverPort))
# Configure it to accept up to N simultaneous Clients waiting...
s.listen(maxConn)


# Run forever
while 1:
    print("Waiting for a connection to %s:%s." % (serverIP, serverPort))
    # wait new Client Connection
    connection, address = s.accept()
    while 1:
        # receive message
        isoStr = connection.recv(2048)
        if isoStr:
            print ("\nInput ASCII |%s|" % isoStr)
            pack = ISO8583()
            # parse the iso
            try:
                if bigEndian:
                    pack.setNetworkISO(isoStr)
                else:
                    pack.setNetworkISO(isoStr, False)

                v1 = pack.getBitsAndValues()
                for v in v1:
                    print (
                        'Bit %s of type %s with value = %r, value_raw = %r'
                        % (v['bit'], v['type'], v['value'], v['value_raw'])
                    )

                if pack.getMTI() == '0800':
                    print ("\tThe client sent a correct message !!!")
                else:
                    print ("The client didn't send the correct message!")
                    break

            except InvalidIso8583 as ii:
                print (ii)
                break

            # send answer
            pack.setMTI('0810')

            if bigEndian:
                ans = pack.getNetworkISO()
            else:
                ans = pack.getNetworkISO(False)

            print ('Sending answer %s' % ans)
            connection.send(ans)

        else:
            break

    # close socket
    connection.close()
    print ("Closed...")
