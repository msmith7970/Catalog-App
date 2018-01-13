
# Udacity's Project 5 - Linux Server Configuration

This project takes a baseline installation of a Linux server and prepares it to host the Catalog Application created in Udacity's Full Stack Web Developer Nanodegree.  Using a Linux server instance from [Amazon Lightsail](https://aws.amazon.com/), it will be set up to be secured from a number of attack vectors, install and configure a web and database server, and deploy the Catalog Application onto it.

* Public IP address: [52.15.211.126](http://52.15.211.126)
* SSH PORT: 2200
* The URL or (Host Name): [ec2-52-15-211-126.us-east-2.compute.amazonaws.com](ec2-52-15-211-126.us-east-2.compute.amazonaws.com)


## Lightsail Server Instance Setup
 Setup a new Ubuntu Linux server instance using Amazon's Lightsail server.
 * Log in to [Lightsail](https://aws.amazon.com/).  If you don't already have an account then create one.
 * Create an Instance. Once logged in, click on the image to "Create an instance".
 * Choose an instance image (a particular software setup) including the operating system and built-in application.  There are two settings.
    - First select "OS Only".
    - Second select "Ubuntu" as the operating system.
 * Choose your instance plan.  The lowest tier of instance will work fine for this project which is the $5 per month plan.
 * Give your instance a hostname.  This instance will need a unique hostname.
 * Give the newly created instance a few minutes to start up for the first time.
 * You can now log into it with SSH from your browser by going to the Connect tab and clicking the orange button that says "Connect using SSH".  You will be logged in as the ubuntu user.  To execute commands as the root user use the sudo command to do it.
 * Click on the Networking tab and click on the orange button "Create static IP" to create a static IP address for this project.


## Secure Your Server
1. Update all currently installed packages.
    Get Package Source List by:

    `$ cat /etc/apt/sources.list`

    Make sure all software is up to date with new releases.  First update your package source list.

    `$ sudo apt-get update`

    This will run thru all the repositories in the sources.list file.  This doesn't make any changes, it just makes your system aware of the new changes that are available.

    Now update the software. This will make the changes to apply the most recent version numbers to the software.

    `$ sudo apt-get upgrade`

    `$ man apt-get` - to see the manual for this command.

    To see if there are any packages that are no longer required that we can remove.

    `$ sudo apt-get autoremove`

    Install finger. A package to lookup and display information about a user.

    `$ sudo apt-get install finger`

    Use `$ finger` or `$ finger [user name]` to see more detailed information about a user.

    To search for other ubuntu packages, go to [packages.ubuntu.com](www.packages.ubuntu.com).

2. Change the SSH port from 22 to 2200.  

    Edit the sshd_confib file to add a line for port 2200.  Once port 2200 is confirmed working come back and delete the line for port 22.

    `$ sudo nano /etc/ssh/sshd_config`

    Around line 4 where is says:
    What ports, IPs and protocols we listen for
    Port 22

    After the line Port 22, add a new line for Port 2200.  So now it looks like:
    ```
    What ports, IPs and protocols we listen for
    Port 22
    Port 2200
    ```
3. Require All Users to Authenticate using RSA Keys

    `$ sudo nano /etc/ssh/sshd_config`

    Look for line with:
    ```
    PasswordAuthentication Yes
    ```
    and make sure it is set to No.
    ```
    PasswordAuthentication No
    ```
    Exit and save the sshd_config file.

    ***
    Note: also make sure both of the following are set to yes
    ```
    RSAAuthentication yes
    PubkeyAuthentication yes
    ```
    ***

    When changes are made to this file, the SSh service will need to be restarted.

    `$ sudo service ssh restart`

4. Block Remote Connections

    `$sudo nano /etc/ssh/sshd_config`

    Change: PermitRootLogin prohibit-password
    To: PermitRootLogin no

    Reference: [Ubuntu:sshd_config](http://manpages.ubuntu.com/manpages/zesty/man5/sshd_config.5.html)

5. Secure Your Uncomplicated Firewall (UFW)
    ```
    $sudo ufw status   - default shows Status: inactive
    $ sudo ufw default deny incoming
    $ sudo ufw default allow outgoing
    $ sudo ufw allow ssh
    $ sudo ufw allow 2200/tcp
    $ sudo ufw allow www
    $ sudo ufw allow ntp - to synchronize the system clock with a trusted external source.
    $ sudo ufw allow out 53 - for outgoing traffic were /etc/ntp.conf contains domain names of NTP servers.
    $ sudo ufw enable
    $ sudo ufw status - to verify our changes.
      Status: active
    ```

    Allow outgoing on port 53 for NTP to access the DNS server.  When finished with changes that are needed and to make these changes go into effect type the following command to restart the SSH service:

    `$ sudo service sshd restart`

6. Secure the Lightsail firewall by configuring it to allow it SSH only on port 2200.  

    The Lightsail external firewall must also be set up by configuring it on the Networking tab on the Lightsail site.  Add a custom rule to allow TCP on port 2200 by clicking the '+ Add Another' link at the bottom.  Leave both port 22 and 2200 for SSH in the rules configuration to keep from getting locked out.  Once you know your access is working on port 2200, then you can delete the line with port 22.  To delete the line with port 22, click the Edit rules button and click the X on the right hand side of the line for port 22.  Click Save.

    Logging back in after Firewalls are set up.  Once both firewalls are set up connect by SSHing in from the local Git Bash terminal with:

    `$ ssh -i ~/.ssh/[keyname.rsa] -p 2200 ubuntu@[static ip address]`


### Install Python
    If Python 2.7 is not installed on the new server, then install python 2.7 to work with the Catalog Application.

    `$ sudo apt-get install python2.7`

    `$ python -V` - To get the version number.
    ubuntu@ip-172-26-8-116:~$ python -V

    Python 2.7.12

    To install PIP:

    `$ sudo apt-get install python-pip`

    `pip --version` - To get the version number.
    ubuntu@ip-172-26-8-116:~$ pip --version

    Result: pip 9.0.1 from /usr/lib/python2.7/dist-packages (python 2.7)


## Build *grader*
Build a user named "grader" and give this user  permission to sudo.  Create an SSH Key Pairs for this user using the ssh-keygen tool.

1. Build user named 'grader'.

    `$ sudo cat /etc/passwd`  - To look at info for all users.

    To Add a user:
    `$ sudo adduser grader`

2. Give user 'grader' sudo permissions.

    `$ sudo cat /etc/sudoers`

    Look for the include file like /etc/sudoers.d
    and update this dir by putting your customization for the 'grader' user in this directory.

    `$ sudo ls /etc/sudoers.d`

    `$ sudo cp /etc/sudoers.d/90-cloud-init-users /etc/sudoers.d/grader` - copy the 90-cloud-init-users file to create a new one named grader.

    `$ sudo nano /etc/sudoers.d/grader`

    Edit this file to change the word ubuntu to grader and save the file.
3. Create an SSH key pair for 'grader' using the *ssh-keygen* tool.  To set up access with a key based authentication generate the key locally on the client.

    `$ ssh-keygen`
    Save it in the default directory on your local machine.  Ex: (/users/usersname/.ssh/id_rsa)

    `~/users/usersname/.ssh/grader)`

    This is the default directory that key pairs should exist in.  Add a passphrase.  This command generates two files. The one titled with .pub is the one that we will put on our server.  The other one will stay on our local machine in this directory.

    To put it on the server. First log in as the user grader.  In the home directory /home/grader:

    `$ mkdir .ssh`

    `$ touch .ssh/authorized_keys` There will only be one key in this file, however additional keys can be add with one key per line in this file.

    `$ sudo nano .ssh/authorized_keys`

    Go back to our local machine and copy the key to be placed in this file.

    `$ cat .ssh/grader.pub` - Copy the contents.

    Back on the server as the grader user.

    `$ nano .ssh/authorized_keys` - Paste the key in this file and save it.

    Set up specific file permissions on the authorized_keys file and the .ssh directory.

    `$ chmod 700 .ssh`

    `$ chmod 644 .ssh/authorized_keys`

    Now you can login as 'grader' using SSH.

    `$ ssh grader@[public ip] -p 2200 -i ~/.ssh/grader`

    `$ ssh grader@52.15.211.126 -p 2200 -i ~/.ssh/grader`


### PuTTY Setup
Instructions for setting up PuTTY to use with the SSH key pair.  

Download PuTTY here: [PuTTY](www.putty.org).

For Reference, Lightsail [instructions](https://lightsail.aws.amazon.com/ls/docs/how-to/article/lightsail-how-to-set-up-putty-to-connect-using-ssh) for PuTTY:

How to set up putty for *grader*:

This is a two step process:

1. First you must convert the private key located on the client to the PuTTY format, which is a file ending with the .ppk extension.

    - Download and Install [PuTTY](www.putty.org).
    - Convert the private key located on the client to the PuTTY format. Open Putty key gen on your PC by Start>Programs>PuTTY>PuTTygen
    - Click the Load button and navigate to your directory containing the key pairs.  The path may look like: `/c/Users/[users name]/.SSH`
    - To the right of the File Name field, click on the pull down menu and select All Files (\*.\*).
    - Select the filename of grader with no file extensions and click the Open button.
    - You are prompted to enter the passphrase for this user.  Enter the provided passphrase and click the OK button.
    - A PuTTYgen Notice window will open.  After reading, click OK.
    - Click File>Save private key
    - Give it the file name grader.ppk (Don't forget to enter the file extension as .ppk so that you don't overwrite the existing file called grader without an extension.)
    - Exit out of PuTTygen with File>Exit.

    In your .ssh folder on your local machine you should now have three files with the same name but with three different file extensions:

            1. grader       - File Type = File
            2. grader.pub   - File Type = Microsoft Publisher Document
            3. grader.ppk   - File Type = PuTTy Private Key File

2. Second, Configure PuTTY with your PuTTy formatted private key and instance information.
    - Open Putty on your PC by Start>All Programs>PuTTY
    - Click on the Session tab.
        - Enter the Public IP address in the Host Name field = 52.15.211.126
        - Enter the Port = 2200
    - Click on Connection>SSH>Auth and click the Browse button.
    - Navigate to the .ppk file containing the PuTTY formated version of the private keypair file you created with PuTTYgen and click Open.  Ex:  `grader.ppk`
    - To Save this configuration to be used later.
        - Click Session.
        - In the Saved Sessions field give it a name and click the Save button.
    - To Open the Session and get the terminal window, click the Open button at the bottom of the Configuration window.

## Setup the Ubuntu User with PuTTY
Set up the Amazon Lightsail ubuntu user on PuTTY.

- Get your Private key Ready.  On your Lightsail Account page, choose Download default private key and save the LightsailPrivateKey-us-east-2.PEM file in your .ssh directory `~/Users/[user name/.ssh]`
- Configure PuTTY with your Lightsail private key by     Start>PuTTy>PuTTYgen
- Choose Load. By default, PuTTYgen displays only files with the .ppk extension. To locate your .PEM file, select the option to display files of all types. Select LightsailDefaultPrivateKey-us-east-2.PEM, and then press Open.
- PuTTYgen confirms that you successfully imported the key, and then you can choose the OK button.
- Choose Save private key, and then confirm you don't want to save it with a passphrase.
- If you choose to create a passphrase as an extra measure of security, remember you will need to enter it every time you connect to your instance using PuTTY.
- Specify a name and a location to save your private key, and then choose Save.
example ~/.ssh/ubuntu.ppk
- Close PuTTYgen.  File>Exit
- Configure the PuTTY session by opening Putty on your PC: Start>All Programs>PuTTY
- Click on Session
- Enter the Public IP address in the Host Name field = 52.15.211.126
- Enter the Port = 2200
- Click on Connection> SSH> Auth and click the Browse button.
- Navigate to the .ppk file containing the PuTTY formated version of the private keypair file you created with PuTTYgen.  Ex:  ubuntu.ppk.
- To Save this configuration to be used later, Click Session
- In the Saved Sessions field give if a name and click the Save button.
- To Open the Session and get the terminal window, click the Saved Session name then click the Open button at the bottom of the window.
- At the prompt on the terminal window: login as: Enter *ubuntu*.


Optionally: To make a SSH connection as the ubuntu user.  From a Gitbash Terminal Window:

`$ ssh ubuntu@52.15.211.126 -p 2200 -i  ~/.ssh/LightsailDefaultPrivateKey-us-east-2.PEM`


## SERVER CONFIGURATION
### Configure the local timezone to UTC
To Verify the timezone and date/timezone

`$ timedatectl`

If not set to UTC, then to change it to UTC:

`$ sudo dpkg-reconfigure tzdata` -  scroll to the bottom of the Continents list and select Etc or None of the above; in the second list, select UTC.

If not configured, then to install NTP:

```
$ sudo apt-get update
$ sudo apt-get install NTP
```

### Install Apache2 Web Server
Install Apache2 using your package manager with the following command:

`$ sudo apt-get install apache2`

Confirm Apache is working by visiting http://52.15.211.126:8080 in your browser.

#### ERROR LOGS
For apache2 webserver:

`$ sudo tail -10 /var/log/apache2/error.log`

TO VIEW IN REAL TIME:

`$ sudo tail -f /var/log/apache2/error.log`

TO SEE BOTH Error and Access LOGS REAL TIME:

`$ sudo tail -f /var/log/apache2/error.log /var/log/apache2/access.log`


### Install mod_wsgi module
This is an interface between the Apache2 web server and Python.  Then enables the Apache2 HTTP server to serve Flask applications.

`$ sudo apt-get install libapache2-mod-wsgi python-dev`

Enable mod_wsgi by:

`sudo a2enmod wsgi`

Start up the Apache2 server:

`sudo service apache2 start`


## INSTALL git

`$ sudo apt-get install git`

### Clone the catalog repository
First cd over to this directory /var/www/html and create a new directory named catalog and clone the catalog repository from github into a new directory called catalog:

```
$ cd /var/www/html
$ mkdir catalog
$ cd catalog
$ git clone https://github.com/msmith7970/Catalog-App.git catalog
```

Rename the downloaded directory Catalog-App to catalog. Now all the files from the repository will be in this directory: /var/www/html/catalog/catalog


## Set up a Virtual Environment to Host the Catalog Application, Install Flask and the applications dependencies

Setup a virtual environment which will keep the Catalog Application separated from the main system.

First two items are needed to be installed globally:

`$ sudo apt-get install python-pip`
`$ sudo pip install virtualenv`

If you get a message that pip can be upgraded to a new version, go ahead and upgrade.

`$ sudo pip install virtualenv --upgrade pip`

The rest will be installed inside the virtual environment which will be called *venv*.  Ex: /etc/www/html/catalog/catalog/venv.  By doing so, this will keep the catalog application and it's dependencies isolated form the main system.  This will allow you to run different applications simultaneously and each can maintain their own separate configuration.

Use the following to name your temporary environment with the name: *venv*
```
$ sudo virtualenv venv
New python executable in /var/www/html/catalog/catalog/venv/bin/python
Installing setuptools, pip, wheel...done.
$
```

Change permissions on this new folder and everything in it:

`sudo chmod -R 777 venv`

Install Flask in that environment by activating the virtual environment:

`$ source venv/bin/activate`

Notice that when you are connected to this virtual environment that the CLI prompt now begins the line with the name of the virtual environment:  

Ex: (venv) ubuntu@ip-172-26-8-116:/var/www/html/catalog/catalog$

Command to install Flask inside that environment:

`$ sudo pip install Flask`

Install all the other dependencies required by the catalog application:

`pip install bleach httplib2 request oauth2client sqlalchemy psycopg2 jinja2`

To deactivate the virtual environment:

'$ deactivate'

To see what packages have been installed:

`pip freeze`

To verify that you are using python inside the virtual environment:

`which python`

Notice that is will show /venv/bin/python

References: [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-run-django-with-mod_wsgi-and-apache-with-a-virtualenv-python-environment-on-a-debian-vps)


## Setup the PostgreSQL Database
### Install and Configure PostgreSQL - Our Server side SQL Database

`$ sudo apt-get install postgresql`

### Create a Database User Named 'catalog' with limited permissions to the catalog application Database
To do this you need to connect to the sql server as the postgres user.

The *catalog* user should not be able to create databases and should be the owner of the *catalog* database.  By default the new user will not be allowed to create databases.

```
$ sudo -u postgres psql
=# CREATE USER catalog WITH PASSWORD 'catalog';
CREATE ROLE
postgres=# \du - To verify
```

### Create a new Database
Create a database with the owner as *catalog*:
```
postgres=# CREATE DATABASE catalog WITH OWNER = catalog;
CREATE DATABASE
postgres=#
postgres=# \l
                                  List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------+----------+----------+-------------+-------------+-----------------------
 catalog   | catalog  | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
```

Make sure remote connections to PostgreSQL are not allowed by checking the configuration file and make changes if necessary to make it look like this:

`$ sudo nano /etc/postgresql/9.5/main/pg_hba.conf`

```
# Database administrative login by Unix domain socket
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                peer
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
```

If changes were made, Restart the psql server:

`$ sudo service postgresql restart`

### Give the User *catalog* limited permissions to the catalog application database.

Secure access within the PostgresSQL with the use of "roles".

Login as postgres and connect to the *catalog* database:

`sudo su - postgres psql`

`\c catalog`

`catalog=# \dp` - To display the priviledges granted on existing table and columns.

```
                                   Access privileges
 Schema |      Name       |   Type   | Access privileges | Column privileges | Policies
--------+-----------------+----------+-------------------+-------------------+----------
 public | category        | table    |                   |                   |
 public | category_id_seq | sequence |                   |                   |
 public | item            | table    |                   |                   |
 public | item_id_seq     | sequence |                   |                   |
 public | user            | table    |                   |                   |
 public | user_id_seq     | sequence |                   |                   |
(6 rows)
```

By default tables are automatically put into the schema called 'public'.

`REVOKE ALL ON SCHEMA public FROM PUBLIC;` - (The first public is the schema and the second PUBLIC refers to every user.)  This will remove all permissions. First connect to the *catalog* database.

```
postgres=# \c catalog
You are now connected to database "catalog" as user "postgres".
catalog=# REVOKE ALL ON SCHEMA public from PUBLIC;
REVOKE
catalog=#
```

`catalog=# GRANT ALL ON SCHEMA public TO catalog;` - This will only allow the role *catalog* to have permissions.

Reference: [Digital Ocean - How To Secure PostgresSQL on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)

### Other useful postgresql commands

- Delete a Database
```
$ sudo -u postgres psql
DROP DATABASE [ IF EXISTS ] name;
$ psql
postgres=# DROP DATABASE IF EXISTS catalog;
```

- Create a Table in the Catalog Database
 `=# CREATE TABLE users;`

- Assign user catalog to the Database catalog
```
=# postgres=# GRANT ALL PRIVILEGES ON DATABASE catalog to catalog;
GRANT
postgres=#
```

- To Connect to a Database:
 `=# \c [Database Name]`

- To List all Databases:
 `=# \l`

- To List all tables
 `=# \d`

- To Describe a table
 `=# \d tablename`

- To View Error Logs for postgresql
 `$ tail -f /var/log/postgresql/postgresql-9.5-main.log`

## Update the Create_Engine to the following 3 files in the Catalog Application:

1. application.py
2. database_setup.py
3. lotsofitems.py

Use the sudo nano to go into each of these files and make the change to the line as shown below:

`$ sudo nano /var/www/html/catalog/database_setup.py`

Change:
engine = create_engine('sqlite:///catalog1.db')

To:
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

From reference at Sqlalchemy site: [http://docs.sqlalchemy.org/en/latest/core/engines.html](http://docs.sqlalchemy.org/en/latest/core/engines.html).

The create_engine() function produces an Engine object based on a URL. These URLs follow RFC-1738, and usually can include username, password, hostname, database name as well as optional keyword arguments for additional configuration. In some cases a file path is accepted, and in others a “data source name” replaces the “host” and “database” portions. The typical form of a database URL is:
dialect+driver://username:password@host:port/database

Note: If for some reason during the setup process it fails, go back and delete the tables that were previously made in the Catalog Database, make the necessary corrections and rerun the database setup by cd over to the directory and run the database_setup.py file.

```
$ cd /var/www/html/catalog/catalog
$ python database_setup.py
```

Now when you connect back to the catalog database you will see three newly created tables category, item and user.
```
$ sudo -u postgres psql
=# \c catalog
catalog-> \dt
          List of relations
 Schema |   Name   | Type  |  Owner
--------+----------+-------+---------
 public | category | table | catalog
 public | item     | table | catalog
 public | user     | table | catalog
(3 rows)
```

To Load the sample catalog data into the catalog databases:
`$ python lotsofitems.py`


# Finish Deploying the Flask Application

1. Creating a Flask App

    - In the /var/www/html/catalog/catalog directory, create a '\__init\__.py' file that will contain the flask application logic.  Use the following as an example to make sure the test message can be seen.  This will confirm the sample application is working.

     `$ sudo nano __init__.py`

    - Add the following logic to the file:

            from flask import Flask
            app = Flask(__name__)
            @app.route("/")
            def hello():
                return "Hello, I love Digital Ocean!"
            if __name__ == "__main__":
                app.run()

    - Save and close the file.
    - Once this example is working come back and either delete all the lines in this file or comment out all the lines.  All that is needed is a blank file named '__init__.py'.

2. Configure and Enable a New Virtual Host to be used by the Apache2 web server.
    - Create a configuration file for the Catalog Application.

    `$ sudo nano /etc/apache2/sites-available/catalog.conf`

    - Paste the following into it:

    ```
    <VirtualHost \*:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        # DocumentRoot /var/www/html
        ServerAlias ec2-52-15-211-126.us-east-2.compute.amazonaws.com
        # Define WSGI parameters.
        RedirectMatch 404 /.git
        WSGIDaemonProcess catalog python-path=/var/www/html/catalog/catalog:/var/www/html/catalog/catalog/venv/lib/python2.7/site-packages
        WSGIProcessGroup catalog
        # WSGIDApplicationGroup %{GLOBAL}
        WSGIApplicationGroup catalog

        # Define the location of the app's WSGI file
        WSGIScriptAlias / /var/www/html/catalog/catalog.wsgi

        <Directory /var/www/html/catalog/catalog/>
                Order allow,deny
                Allow from all
        </Directory>
        Alias /static /var/www/html/catalog/catalog/static
        <Directory /var/www/html/catalog/catalog/static/>
                Order allow,deny
                Allow from all
        </Directory>

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf

    </VirtualHost>
    ```

    - Save and close the file.
    - Enable the virtual host.  First, Verify if any other configuration files are enabled by listing the contents of this directory:

    `$ ls /etc/apache2/sites-enabled`

    If there are any then you and disable that configuration file by:

    Ex: `sudo a2dissite 000-deault.conf`

    Then enable our new one:

    `$ sudo a2ensite catalog`

    To make these changes go into effect reload apache:

    `$ sudo service apache2 reload`

    To status the apache server:

    ```
    $ sudo /etc/init.d/apache2 status
     * apache2 is running
    ```

    May need to use $journalctl | tail to troubleshoot if apache fails to reload.

    ### Make the .git Directory Publicly Inaccessible From a Browser.

        `$ sudo nano /etc/apache2/sites-enabled/catalog.conf`

        Add the following line above the WSGIDaemonProcess line:

        `RedirectMatch 404 /.git`

        Save file and restart apache2 service

        `$ sudo apache2ctl restart`

3. Create the .wsgi File
    Apache uses the .wsgi file to serve the Flask app. Move to the /var/www/catalog directory and create a file named catalog.wsgi:

    ```
    $ cd /var/www/html/catalog
    $ sudo nano catalog.wsgi
    ```

    Add the following lines:
    ```
    #!/usr/bin/python
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,'/var/www/html/catalog')

    from catalog.application import app as application
    application.secret_key = 'super_secret_key'
    ```

    Save and close.

    Now your directory structure should look like this:

    ```
    |--------catalog
    |----------------catalog
    |-----------------------static
    |-----------------------templates
    |-----------------------venv
    |-----------------------__init__.py
    |----------------catalog.wsgi
    ```

    Finally Restart Apache:

    `$ sudo service apache2 Restart`


# Fix client secrets file for Google OAuth
- In /var/www/html/catalog/catalog/application.py
    ```
    Change:
    # Use Google Account Info for secure connection
    CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']

    To:

    # Use Google Account Info for secure connection
    - In the application.py file make:

        CLIENT_ID = json.loads(
        open(r'/var/www/html/catalog/catalog/client_secrets.json', 'r').read())['web']['client_id']
    ```

- client_secrets.json

    Also changed:

    /var/www/html/catalog/catalog/client_secrets.json

    "javascript_origins":["http://52.15.211.126", http://ec2-52-15-211-126.us-east-2.compute.amazonaws.com"]}}

- Next go to the Google Console
    - APIs & Services>Credentials
    - Under Oauth 2.0 client IDs click on Catalog App
    - For Authorized JavaScript origins enter in http://51.15.211.126 and http://ec2-52-15-211-126.us-east-2.compute.amazonaws.com
    - For Authorized redirect URIs enter in http://ec2-52-15-211-126.us-east-2.compute.amazonaws.com/ouath2callback
    - Hit Save
    - In application.py change line 70 from:
    oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
    to:
     oauth_flow = flow_from_clientsecrets(r'/var/www/html/catalog/catalog/client_secrets.json', scope='')


# Fix client secrets file for Facebook OAuth
- fb_client_secrets.json
    ```
    Change:
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']

    To:
    app_id = json.loads(open(r'/var/www/html/catalog/catalog/fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open(r'/var/www/html/catalog/catalog/fb_client_secrets.json', 'r').read())['web']['app_secret']
    ```

Make changes on Facebook Developers site:
    https://developers.facebook.com/products
- Click on My Apps and select the Catalog App Project. Go to the settings>basic tab
    - Under Website, change the Site URL from http://localhost:8000/ to :
    ec2-52-15-211-126.us-east-2.compute.amazonaws.com
    - In the Privacy Policy URL field, enter http://52.15.211.126
- Go to the Facebook Login tab and select settings.
    For the Valid OAuth redirect URIs enter in both:
    http://ec2-52-15-211-126.us-east-2.compute.amazonaws.com
    and
    http://52.15.211.126/
- Click Save Changes button


# Run the Catalog Application

- `$ sudo service apache2 restart`

- Visit the URL: http://52.15.211.126



# Other References
- SSh Keys: [https://help.ubuntu.com/community/SSH/OpenSSH/Keys](https://help.ubuntu.com/community/SSH/OpenSSH/Keys)
- Appache Documentation: [https://httpd.apache.org/docs/2.2/configuring.html](https://httpd.apache.org/docs/2.2/configuring.html)
- PostgreSQL Documentation: [htts://www.postgresql.org/doc/9.3/static/index.html](htts://www.postgresql.org/doc/9.3/static/index.html)
- Apache Directive RedirectMatch: [https://httpd.apache.org/docs/2.2/mod/mod_alias.html#redirectmatch](https://httpd.apache.org/docs/2.2/mod/mod_alias.html#redirectmatch)
- Sqlalchemy Engine Configuration:
[http://docs.sqlalchemy.org/en/latest/core/engines.html](http://docs.sqlalchemy.org/en/latest/core/engines.html)
- How To Deploy a Flask Application on an Ubuntu VPS:
    [https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
- modwsgi-ConfigurationDirectives.wiki:
    [https://code.google.com/archive/p/modwsgi/wikis/ConfigurationDirectives.wiki](https://code.google.com/archive/p/modwsgi/wikis/ConfigurationDirectives.wiki)
- To find a host name given the ip address:
    [http://www.hcidata.info/host2ip.cgi](http://www.hcidata.info/host2ip.cgi)
- The pg_hba.conf file:
    [http://www.linuxtopia.org/online_books/database_guides/Practical_PostgreSQL_database/c15679_002.htm](http://www.linuxtopia.org/online_books/database_guides/Practical_PostgreSQL_database/c15679_002.htm)
- How To Install Apaceh2 Web Server on Ubuntu: [https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-16-04](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-16-04)
- Udacity discussions:
    - [https://discussions.udacity.com/t/web-error-wsgi/223480/3](https://discussions.udacity.com/t/web-error-wsgi/223480/3)
    - [https://discussions.udacity.com/t/how-to-connect-wsgi-to-psql/396306/4](https://discussions.udacity.com/t/how-to-connect-wsgi-to-psql/396306/4)
- How to Use Roles and Manage Grant Permissions in PostgresSQL on a VP: [https://www.digitalocean.com/community/tutorials/how-to-use-roles-and-manage-grant-permissions-in-postgresql-on-a-vps--2](https://www.digitalocean.com/community/tutorials/how-to-use-roles-and-manage-grant-permissions-in-postgresql-on-a-vps--2)
- Virtual Environments by:  [dabapps](https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/)


## License

The content of this repository is licensed under MIT License.

Copyright (c) 2018 Mitchell Smith

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
