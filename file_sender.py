import pysftp
from connector import Connector
#NOTE: Connector class just sets up sftp connection with my webserver.
#Example: connection = pysftp.Connection(
#             host="server", 
#             username="username", 
#             private_key="path_to_key", 
#             private_key_pass="password"
#           )
# Look up documentation for pysftp for more information on how to do this.
#
# I did not do that part here as this file is going to be uploaded to the
# github repo, which would present a security risk.

class Sender():
		
	def send(self, server_path, local_file):
		
		try:
			#Get the connection to the web server
			connector = Connector()
			sftp = connector.getConnection()
			
			#Place file in web server
			with sftp.cd(server_path):
				sftp.put(local_file, confirm=True)
			
			return 1
			
		except Exception as e:
			print("Problem sending file")
			with open('log.txt', 'a') as log:
				log.write("Problem sending file\n")
				log.write(repr(e))
			print(e)
			return 0
		
