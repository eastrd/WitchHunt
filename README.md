# WitchHunt (猎巫)
##### This honeypot is used for fast tracking e-identity information of the prey.
<br /><br />
TODO:
<br />
- Add attack modules for user device exploitation (ref. BeeF framework)
- Wechat: Add honeypots via messaging & Notification
- Add Analysis module for the prey information (Common IPs recognition)
- Add Status Code as an option.
- Add Reverse Proxy as an setup option
- Beautify UI
<br /> <br /> <br />

DONE:
<br />
- Test SendEmail function. (Tested & Added Error handling functionality)
- Implement expiry time logic for traps. (Done, also added conditional checks to clean DB)
<br /> <br />


##### It features the following compare to a traditional honeypot:
- Setting up via any portable mobile device
- Super fast setup process
- Customize honeypot webpage source code
- Automatically obtain the prey's physical location and ISP information
- Precise email notification when the trap is triggered
- Pre-set the valid expiry time for the webpage (Yet to be implemented)

<br />

How-To:
- Goto `http://your-site-here.com/set` to config and add new honeypots.

<br />

Installation:
- Install Python 3.X on your machine. ( e.g. 3.5.3 )
- `pip install flask dataset selenium`
- Get PhantomJS:
 - Windows: https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip , unzip the phantomjs.exe and put it under the WitchHunt directory.
 - Linux: `apt-get install phantomjs`

<br /><br />
