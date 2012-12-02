Welcome! This repository contains tools for visualizing changes to code over time. The workhorse here is `FileTimeline.py`, a [Python][1] script designed to help visualize changes made to a single file of code. 

## Requirements for using these tools ##

In order to run our tools properly, you're going to need a few things. But don't worry! Below, we explain how to get all of them:

- A working version of [Python][1]. The tools were developed on Python 2.7.3, and in principle should work with Pyhon 3.x installations, but I can't make any guarantees.
- The [GitPython][3] and [pystache][5] libraries for Python (installation instructions below)
- A code file of interest that's currently under version control in a [Git][2] repository
- A stable, recent release of a major browser (we try to test on Chrome, Safari, and Firefox, in that order)

## How to get set up ##

## On Windows ##

We don't have separate instructions for Windows right now, because I can't currently test on a windows machine. But! But! You're welcome to try the Mac/Unix directions below, modify them where appropriate, and [open an issue][8] if you can't adapt them to work for your windows system.

### On Mac/Linux/Unix-based systems

1. Make sure you've got [Git][2], 
2. Then, open a terminal, clone our stuff, and navigate to it:
		
	```bash
	$ cd path/to/where/you/want/our/stuff
	$ git clone https://github.com/briandk/gitvisualizations.git
	$ cd gitvisualizations
	```

3. Make sure you [have Python Installed][6]

	```bash
	$ which python # should return python's location, if it's installed
	```

4. [Install pip][7] if you haven't got it already

	```bash
	$ which pip # should return pip's location, if it's installed
	```

5. Use pip to install the required python dependencies for this project

	```bash
	$ pip install -r requirements.txt
	```

6. You should be good to go! Assuming your terminal prompt is still in the `gitvisualizations` project directory, you can start using it like so:

	```bash
	$ python FileTimeline.py ~/ReallyInterestingCodeYouHave.c
	```

## Let us know what you think

Please give us feedback! We'd love to hear your gripes, thrill stories, and feature requests. Just [open an issue][8] to get in touch. Thanks!

[1]: http://python.org/
[2]: http://git-scm.com
[3]: http://pypi.python.org/pypi/GitPython/0.3.2.RC1
[4]: http://mxcl.github.com/homebrew/
[5]: http://pypi.python.org/pypi/pystache
[6]: http://wiki.python.org/moin/BeginnersGuide/Download
[7]: http://www.pip-installer.org/en/latest/installing.html
[8]: https://github.com/briandk/gitvisualizations/issues/new