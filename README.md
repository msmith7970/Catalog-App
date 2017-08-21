## SCOPE

The purpose of the project is to create a Web Application for a Catalog.  This catalog will provide a list of items for a variety of Categories.  The Catalog app will provide a third party user registration using Google and Facebook.  Authenticated users will have the ability to add, edit and delete their own categories and items.  This application will also utilize Flask and sqlite.  Once installed and setup this application can be accessed by visiting http://localhost:8000 locally on your browser.


## Usability

The application can be downloaded by going to GitHub at:
[Catalog Web Application](https://github.com/msmith7970/Catalog-App)

The home page will display the public's version of the Catalog APP.  The home page will also show a list of all Categories available in the Catalog along with a list of the latest 10 items added to the Catalog. Next to the latest item added in parenthesis will be the corresponding Category that it belongs to.

A user will have the option to login using a third party user registration using either Google or Facebook.  Once logged in the user will have the ability to Add, Edit or Delete either Categories or Items in a category but only if they are the original creator of those Categories or Items.

A catalog database 'catalog1.db' will be provided to allow the user to view sample data for the Catalog.

Data for this project is stored in three databases:
    1. Users - Containing a Users name, URL to their picture, an id and email address.
    2. Category - Category name and user id of the creator.
    3. Item - Item name, item description, category name, user id of the creator.


## Setup

On your PC you will need to have the following Applications Set up and
Installed:

* Install [Python](https://www.python.org/downloads/).
* Install [VirtualBox](https://www.virtualbox.org/). Instructions can be found on their website.  VirtualBox is the software that runs the VM (virtual machine)
* Install [Vagrant](https://www.vagrantup.com/).  Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.
* Install [Jinja](http://jinja.pocoo.org/).  Jinja is used to create templates
 and helper functions.
* Install [SQLAlchemy](http://www.sqlalchemy.org/).  On the installed Vagrant machine.  At the vagrant prompt type $ sudo apt-get install python-sqlalchemy.  If you get an error follow what the error message says or visit the sqlachemy website for more info.
* Install and Set up [Git](https://help.github.com/articles/set-up-git/).  The Git Bash program is installed with Git.  This will get you a Unix-style terminal.


## Download Files From GitHUb

Download and install the following items from GitHUb to a PC that can be viewed
using the Google [Chrome](https://www.google.com/chrome/browser/) Web Browser.

These items include:

    1) The Python files.
      * application.py - This is the main python program for the Cataglog App.
      * database_setup.py - This python file defines how the databases are setup.
      * client_secrets.json - Contains the Google token setup.
      * fb_client_secrets.json - Contains the Facebook token setup.
      * listofitems.py - This contains sample data for the database.
    2) Templates Directory - This directory contains all of the web templates used in the Catalog App.  
    3) Static Directory - Contains the CSS file used for custom styling of the Application.
    4) README.md


## To configure the application on your PC

* Get all the items from Setup listed above installed and running.

* Create a new folder on your PC in the vagrant directory that will be used to clone the Catalog App GitHub repository into locally on your machine.

* Open a GitBash command line editor on your PC and navigate to the directory you created in the previous step.

* Clone the GitHub repository into this newly created folder by doing the
following:

 1. Goto GitHub at [https://github.com/msmith7970/Catalog-App](https://github.com/msmith7970/Catalog-App)
 2. Under the repository name, Click "Clone or download"
 3. In the Clone with HTTP section, click the "Copy to clip board" option to
copy the clone URL for the repository.
 4. Open Git Bash and navigate to the folder you created to store the repository
in.
 5. Type ** git clone ** and then past the URL you copied.  It will look like the
following:

          $ git clone https://github.com/msmith7970/Catalog-App

 6.  Press **Enter** and your local clone will be created.  You will now have a
local copy of your fork of the Catalog App repository.


* On the command line editor in your new directory, start the Vagrant machine by typing the following:

      > vagrant up - To start the virtual machine.
      > vagrant status - If you want to check the status of the vagrant machine and verify that it has started with no errors.
      > vagrant ssh - to connect to the virtual machine.
      > cd /vagrant - this vagrant directory allows the virtual machine to share files with your host machine.  Navigate to the folder containing the Catalog App.
      > python database_setup.py - To initialize the databases if you do not want to use the "cataglog1.db" provided as an example.
      > python listofitems.py - To load the Catalog data into the appropriate databases just initialized.
      > python application.py - to start the Catalog App.


* Open Google Chrome browser and navigate to the local server by typing the
following URL:

      http://localhost:8000

* You are now connected to the Catalog App.

* To stop the Catalog Web Application.

      > Control-C - Use the Control-C in the Gib Bash window were the application.py file is running.  This will terminate the program from running.
      > vagrant halt - To stop the virtual machine.
      > exit - To close the window.

## Google Chrome

To install Google Chrome, visit:
[Google Chrome](http://www.browserwin.com/web/ "Google Chrome")
and follow the download instructions.


## License

The content of this repository is licensed under MIT License.

Copyright (c) 2017 Mitchell Smith

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
