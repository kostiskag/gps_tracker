"""
gps_logger.py logs received gps points in a local file.
"""

__author__ = "Konstantinos Kagiampakis"
__license__ = """ 
Creative Commons Attribution 4.0 International
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode
"""

import gpsd
import json
import time
import sys
from daemon import Daemon

class MyDaemon(Daemon):
   def run(self):
      STEP = 3
      # Connect to the local gpsd
      while True:
         try:
            print("Connecting on GPSD...")
            gpsd.connect()      
         except:
            print("Could not connect to GPSD.\nThis script is persistent and will try to reconnect to GPSD in 10 sec.",sys.exc_info()[0])
            time.sleep(10)
         else:
            print("GPSD connected!")
            break
      
      filename = "/home/pi/gps_route.log"
      try:
         f = open(filename, 'a')  
      except:
         raise
      
      while True:
         try:
            try:
              packet = gpsd.get_current()
              
              if packet.mode > 1:           
                 if packet.mode >= 2:
                    print("Latitude: " + str(packet.lat))
                    print("Longitude: " + str(packet.lon))
                    print("Track: " + str(packet.track))
                    print("Horizontal Speed: " + str(packet.hspeed))
                    print("Time: " + str(packet.time))
                    print("Error: " + str(packet.error))
                 if packet.mode == 3:
                    print("Altitude: " + str(packet.alt))
                    print("Climb: " + str(packet.climb))
                    
                 point = {'lat': str(packet.lat), 'lon': str(packet.lon),  'track': str(packet.track), 'hspeed': str(packet.hspeed), 'time': str(packet.time)}
                 if packet.mode == 3:
                   point['alt'] = str(packet.alt)
                   point['climb'] = str(packet.climb)
        
                 str_point = json.dumps(point)
                 print("storing point to file:#"+str_point+"# str len:"+str(len(str_point)))

                 try:
                    f = open(filename, 'a')
                 except:
                    pass
                 else:
                    try:
                       f.write(str_point+',\n')
                    except:
                       pass
                    f.close()
                 
              else:
                 print("There is no GPS FIX yet. Packet mode 0.")
                 time.sleep(10)
            
            except (NameError, KeyError): 
               print("There is no GPS FIX yet. Key or Name exception.")
               time.sleep(3) 
            except:
               print (sys.exc_info()[0]) 
               time.sleep(10)      
            
            time.sleep(STEP)
         
         except KeyboardInterrupt:
            print(" Received KeyboardInterrupt")
            break
         except:
            print(sys.exc_info()[0])
            break      

if __name__ == "__main__":
        daemon = MyDaemon('/tmp/d-gps-logger.pid','/dev/null','/home/pi/stdout','/home/pi/stderr')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print ("Unknown command")
                        sys.exit(2)
                sys.exit(0)
        else:
                print ("usage: %s start|stop|restart" % sys.argv[0])
                sys.exit(2)
               
