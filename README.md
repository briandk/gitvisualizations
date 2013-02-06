Welcome! This repository contains tools for visualizing changes to code over time.

## Requirements for using these tools ##

In order to run our tools properly, you're going to need a few things. But don't worry! Below, we explain how to get all of them:

### Python Requirements

- A working version of [Python][1]. The tools were developed on Python 2.7.3, and in principle should work with Pyhon 3.x installations, but I can't make any guarantees.
- The [GitPython][3] and [pystache][5] libraries for Python (installation instructions below)
- A code file of interest that's currently under version control in a [Git][2] repository
- A stable, recent release of a major browser (we try to test on Chrome, Safari, and Firefox, in that order)

### R Requirements

You'll need the latest version of R (>= 2.15.2).

You'll also need to install the following dependent libraries from CRAN:

- ggplot2
- plyr
- lubridate

## How to get set up ##

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

5. From your clone of our project directory, use pip to install the required python dependencies for this project

    ```bash
    $ pip install -r requirements.txt
    ```

## RepoStatistics.py Usage

Assuming your terminal prompt is still in the `gitvisualizations` project directory, you can start using `RepoStatistics.py` like so:
  
```bash
$ python RepoStatistics/RepoStatistics.py path_to_another_git_repository
```

### Limiting Date Ranges

You can also specify delimiting dates and times, using the `--since` and `--until` flags. They offer [enormous flexibility][9]

```bash
$ python python RepoStatistics/RepoStatistics.py your_repo --since='2011-01-27'
$ python RepoStatistics/RepoStatistics.py your_repo --until='yesterday'
```

You can even combine both flags (naturally):

```bash
$ python RepoStatistics/RepoStatistics.py your_repo --since='2011-01-27' --until=`yesterday`
```


## Sample Output Graphics

### Commit Activity Summary Plot

In this plot, the blue ribbon bins the total number of commits per day. The red curve shows the cumulative sum of commits over time.

![CommitActivityOverTime-1](https://f.cloud.github.com/assets/330036/130325/80a3c67a-7014-11e2-8088-eb696e35fd51.png)

### Small multiple summary of per-file additions and deletions
This plot shows a small multiple for each unique file in the project. The green ribbon represents total number of lines added per day. The orange ribbon is total number of deletions per day.

![Small Multiple Summary](https://f.cloud.github.com/assets/330036/130328/a10e761c-7014-11e2-8de2-53d293812b07.png)

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
[9]: http://www.kernel.org/pub/software/scm/git/docs/git-log.html#_examples