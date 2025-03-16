DLBDSOOFPP01 Habit Tracking Python Project.

# Habitt - A Habit Tracking App

**Habitt** is a user-focused habit tracking app that leverages JSON storage, Object-Oriented Programming (OOP), and Functional Programming (FP) principles to provide a seamless and efficient habit-tracking experience.

## Features

- **Track daily & weekly habits** with an intuitive JSON-based database.
- **Automatic streak tracking** with dynamic history generation.
- **Simple web interface** powered by Flask.
- **Fully testable** with `pytest`.

---

## Installation & Setup

### 1.0 Clone the Repository

```sh
git clone https://github.com/AmeerNAS/Python-Proj
cd Python-Proj
```

- 1.1 Or Alternatively, Download the Repo from Github:

  Firstly, go to the top of the page, then searching for the Green `<> Code` button which should by o the top right of the repo preview window.

  Secondly, open it to choose **dowload ZIP** which will download the repo as a zipped folder.

### 2.0 Install Dependencies

Make sure you have Python 3.9 or higher
by running:

```sh
py --version #Windows OS
# OR
python3 --version # Linux / macOS
```

installed before continuing.
If you do then, run:

```sh
pip install -r requirements.txt
```

### 3.0 Starting the server

After changing directories to the repo's directory:
To start the app locally, run: (This runs the app with `Debug mode = False`)

```sh
py run.py       # Windows
# OR
python3 run.py  # macOS / Linux
```

- If the command was successful. The app will be available at your localhost.

Simply open:
http://127.0.0.1:8000

- 3.1: Server Bootup Issue:

  Note that, if the app does not open at this exact port or opens but doesn't load anything, that may be caused by your `port 8000` being utilized by another host or server and you will need to free that port or select a new port server port to bypass the issue

## Packaged Tests

To run the test suite, simply execute: (while inside the Python-Proj directory)

```sh
pytest .
```

This will automatically discover and run all tests inside the repo.

## Additionally

The Web app has a simple UI that allows for instant _~satisfaction~_ with its simplicity and clean _~aesthetic~._

Many features are easy to understand and up to standard. However, It is recommended to initially using the Seed Data for the first time use as it provides a randomly generated database which allows you to explore all the features of the app from the get-go!

### How to get Seed Data?

As you open the website for the first time, you should see a `No Data? Get Seed Data!` green button right in **Habits: Daily** habits segment.

Simply click on it and it will generate a complete new database along with 4 weeks worth of data for trial and experimentation.
