# SMTPnotifier
Interface between IP camera email alert and Shinobi CCTV system

Hello and welcome!

Since every camera have now a motion detection, why use CPU for that?
I have couple of cameras, mostly chinese cheap crap. All of them have ability to detect motion and send email with that, and i have decided to use that to my advantage.

I have made a python script that is listening on port 25 for TCP connections, when such connection appears, the script then report to Shinobi via API an event.

port 25 is for mail clients to connect to send emails, and i have configured all my cameras to send an email when there is a motion detected.
There is no passwords or anything, i have tested it with couple cameras and all of them have accepted when i only entered ip address of the server as a email notification setting.
To push the data to the Shinobi i am using official API: https://shinobi.video/docs/api#content-trigger-a-motion-event

The system contains of three files, main config, camera/monitor config and the python script

main config file: config.py
-------------------------------------------------------------------
cfg = {
	"ShinobiHost" : "127.0.0.1",
	"ShinobiPort" : "8080",
	"APIkey" : "zMm9qH234gfsa3t9J4TTi45zopFI1XmT",
	"SMTPip" : "192.168.1.10",
	"SMTPport" : "25",
	"GroupKey" : "3iL4gfw3rZ8"
}
-------------------------------------------------------------------
ShinobiHost - address of the shinobi server, and port
APIkey - api key of your shinobi server, to generate one go main menu -> API -> type IP of your machine from which you will be sending requests or type 0.0.0.0 for everyone's access and cklick add, then you will be granted with an API key
SMTPip - ip addres on which the script will listen for connections from ipcam, this address should be in a subnet with cameras or be within reachable network, this is the address that you should also put in camera email settings
SMTPport - leave it 25 or change it, it should be the same on the camera
GroupKey - main menu -> settings -> account info
And this is all for the main config, remember to put the data inside "" and end each line with the "  ,  "

monitors.csv
-------------------------------------------------------------------
ip,id,plug,name

192.168.1.11,C452Xsdfjk3,test,test
-------------------------------------------------------------------
This is a CSV file to list all cameras that you want to report for.
Each camera is a new row, and within row, each value is separated by comma.
First value is ip address of a camera, to identify it
Then is the Monitor ID, for given camera go Edit Monitor -> Identity and there will be monitor ID
next two values are in the documentation and i do not know what system is doing with them but i am putting there the same name as i have for given camera
Remember that the first line of this file should be: "ip,id,plug,name"

In order for all of that to work, each camera need to have motion detection turned on. To do that, in monitor editor, on the low right corner you have to set setting to advanced and go to Global Detector Settings.
In Detector settings set Enabled: Yes, Allow API Trigger: Always, Send Frames: No, Save Events to SQL: Yes
Leave rest as default, now Shinobi can accept motion events from API.

To view those events you can use power viewer. And to adjust the motion settings you have to set it in camera, but even for the most obscure and cheap aliexpress cameras it is working as charm. 
