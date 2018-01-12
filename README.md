# WitchHunt (猎巫)
##### This honeypot is used for fast tracking e-identity information of the prey.
<br /><br />
TODO:
<br />
- Implement expiry time logic for traps.
- Test SendEmail function.
- Add Status Code as an option.
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
_____________
<br /><br />

##### 此蜜罐旨在用于快速锁定猎物的网络身份信息。
<br /><br />
相比于传统的蜜罐，猎巫蜜罐有如下特点：
- 可利用任意移动设备进行部署
- 高效快速的搭建蜜罐
- 可自定义蜜罐页面的模板源码
- 自动获取猎物的物理坐标信息及ISP信息
- 陷阱被触发时会进行精确邮件通知
- 预设蜜罐页面有效时间期限 （尚未完成）

<br />

蜜罐部署页面：
- 进入 `http://your-site-here.com/set` 来添加并设置新蜜罐页。

<br />

安装说明：
- 安装Python 3.X环境。（比如我的是3.5.3)
- 命令行： `pip install flask dataset selenium`
- 安装PhantomJS:
 - Windows:  https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip , 解压 phantomjs.exe，丢到猎巫目录下。
 - Linux: `apt-get install phantomjs`
---------------------
### 中文说明Bonus:

<br />

 工具运行：

 - 运行环境: `Python 3.X`
 - 需要安装的Python模块：`selenium, dataset, flask`
 - 需要配置PhantomJS驱动
 - 程序目录下，执行`python run.py`，运行web系统
 进入`/set`目录执行蜜罐系统的设定
 - 完成后，例如：一旦设定的`test.php?id=2`被访问，绑定账户就会收到相应邮件

<br /><br />
###### 已采用GPL开源证书
#### 开发者：苍冥 (Github ID: eastrd)
