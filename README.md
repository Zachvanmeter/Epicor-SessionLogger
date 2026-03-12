**Session Management and Logs**
![image|657x383, 100%](upload://6mWqe6HZhf6FHsj6GbhXllmMCPI.png)

We recently added a company, and that means adding licenses, and then negotiating who pays for how many licenses when we inevitably exceed our usage limit. So, I made a python script to log our license usage via REST, and to create a summary file.


**What do you need to do to set it up?**
You need to open SessionLogger.py with a text editor and fill out the needed variables as seen in this image.
![image|690x165](upload://kuyD7cNVX67JydAp20nKChNg311.png)

You will also need to set up an API Key in Epicor.
![image|475x282](upload://zNQjOoccgGPGIDAatAZYsCdoP2Q.png)

The end result is a spreadsheet which can be used to create graphics like this one.

![image|656x385](upload://bF5k0japplRuOjERp7K3aQ3VQNL.png)

Anyway, here is the file!
