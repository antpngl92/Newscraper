# Newscraper

This assumes that you're using Ubuntu Linux for the installation:

1) Installing the Python tools needed for the enviroment

Open up the Terminal Application and start typing the following:

```$ sudo apt-get install python-pip python-virtualenv python-setuptools python-dev build-essential python3.6```

2) Installing the virtual enviroment

```$ sudo pip install virtualenv```

3) Making the directories for the project 

```$ mkdir ~/Dev```

```$ cd ~/Dev```

```$ mkdir venv && cd venv ```

```$ virtualenv -p python3.6 . ```

4) Now we test if Virtual Enviroment has been installed

``` $ cd ~/Dev/venv/ ```

``` $ source bin/activate```

If it worked, you'll see your terminal has (venv) at the beginning. Now we deactivate it by typing in:

```$ deactivate```

5) Now we install Django and the other libraries

Go to your directory that "/Dev/venv" is located and execute

```$ source bin/activate```
(this is to activate the virtual enviroment)

```$ pip install django==3.0.3```
(install the version of Django we're using)

```$ sudo apt-get install python-selenium python3-selenium```
```$ pip install bs4```

(these are the libraries that we are using)

6) And finally, to run the Webscraper

```$ cd src```
```$ python3 manage.py runserver```

This will run it on localhost (you can open the link it gives in the terminal) on your PC for you to use.
