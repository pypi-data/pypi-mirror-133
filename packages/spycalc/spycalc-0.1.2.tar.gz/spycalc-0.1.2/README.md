# spycalc
Extensibly scriptable calculator

this repository is a complete redesign of my previous project, [nscalc](https://github.com/Krayfighter/nscalc)


## Supported Platforms

spycalc is written in pure python, so in theory it should run on
any system, but it is only tested on Windows 10, and Linux (arch)


# Installation


## Cross-Platform

This is the prefered way of installing if you do not really know what you are doing.
This also assumes that you have no prerequisites like python, pip, git, or any other dev tools


### Windows

The first step here is to install python from the microsoft store.

It is recommended that you install python 3.10

![search for python](https://raw.githubusercontent.com/Krayfighter/spycalc/main/images/ms_store_1.png)

click the "Get" button, this will then show, and "Install" button, click that button to install python

![install python](https://raw.githubusercontent.com/Krayfighter/spycalc/main/images/ms_store_2.png)

you may now close that window

the next step is to install spycalc via python's package manager, pip. If you do know what that means, that is ok, just make sure to read the instructions carefully.

Now, type "power" into the "type here to search" bar on the bottom left of your screen, and run powershell as administrator

![launch powershell](https://raw.githubusercontent.com/Krayfighter/spycalc/main/images/ms_pwshl_0.png)

![powershell](https://raw.githubusercontent.com/Krayfighter/spycalc/main/images/ms_pwshl_1.png)

It will bring up a blue screen with white text.
copy the following text and paste it into the
powershell window, and press enter

```powershell
pip install spycalc
```

this will run a command that is pretty intuitive.
it tells 'pip' to 'install' 'spycalc'

![pip](https://raw.githubusercontent.com/Krayfighter/spycalc/main/images/ms_pwshl_2.png "copy/pasting the command")

![command output](https://raw.githubusercontent.com/Krayfighter/spycalc/main/images/ms_pwshl_3.png)

Now, you have install spycalc on your system.

#### currently only runnable via terminal

```powershell
py -m spycalc
```


### Linux


#### arch

sudo pacman -S python3

python3 -m pip install spycalc

#### deb+

sudo apt install python3

python3 -m pip install spycalc


#### running

run using ```python3 -m spycalc```


## Development Mode

This is recommended for those who intend to extend, or fork spycalc

copy the git repository

```bash
git clone https://github.com/Krayfighter/spycalc.git
cd spycalc
pip install pyqt5, sympy
./run.sh # run.sh is a basic run script
```

This may need work in the future but works for now
