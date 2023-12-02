### :wrench: Setting up 

#### 1. Clone the repository

```bash
git clone https://github.com/AroraKaran19/Food-For-All
```

#### 2. Install dependencies

##### a. Install Python on your system

> Skip this step if you already have Python 3.6+ on your system.

###### Windows

Download the latest version of Python for Windows from [here](https://www.python.org/downloads/windows/)

or 

```powershell
winget install -e -i --id=Python.Python.3 --source=winget --scope=machine
```

###### Linux

Python comes pre-installed on most Linux distributions. To check if you have it installed (and which version it is), open a terminal and type the following command:

```bash
python3 --version
```

On Ubuntu/Debian/Pop!_OS, you might need to install the `python-is-python3` package to make `/usr/bin/python` point to `python3` instead of `python2`. To install it, run the following command:

```bash
sudo apt install python-is-python3
```

##### b. Install required python packages/libraries

> It is recommended to use a [virtual environment](https://docs.python.org/3/library/venv.html) for development.

```bash
pip install -r requirements.txt
```

If you are on Linux, you need to install tkinter separately since Python installations on Linux don't come with tkinter by default.


```bash
# for Debian/Ubuntu
sudo apt-get install python3-tk

# for Fedora
sudo dnf install python3-tkinter

# for Arch Linux
sudo pacman -S tk

# for RHEL/CentOS
sudo yum install python3-tkinter
```

If you are MacOS and tkinter doesn't work visit [this](https://www.python.org/download/mac/tcltk/)

##### c. Set up Firebase

1. Create a new project on [Firebase](https://console.firebase.google.com/)
2. Go to Realtime Database and create a new database
3. Copy the URL of the database and save it in a new file called `firebase_url.txt` 
4. Go to Project Settings > Service Accounts select Python and click on Generate new private key. This will download a JSON file containing your service account key.
5. Rename the downloaded JSON file to `key.json`
6. In the root directory of the project, create a new directory called `keys` and move the downloaded JSON file and the `firebase_url.txt` file into it.
7. You should be able to access the database from your Python code now.

### :rocket: Running 

```bash
python main.py
```






