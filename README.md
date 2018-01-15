# WitchHunt (猎巫)
##### This honeypot is used for fast tracking e-identity information of the prey.
<br /><br />
TODO:
<br />
- Implement expiry time logic for traps.
- Test SendEmail function.
- Add Status Code as an option.
- Add Analysis module for the prey information
- Beautify UI
<br /> <br /> <br />

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
