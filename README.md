# AppDynamics User Report

A utility written in Python to see who has logged into the AppDynamics controller in the last week using the AppDynamics REST API.

## Usage

Build the docker container user

`docker build -t name_this .`

Update the configuration.py file with the auth header string.

Needs to have persistent storage locally using the `-v` switch. So then you can run it using:

`docker run -it -v /path/to/reports/:/project container_name python3 /project/UserReport.py`

2 reports are included for examples.

## To Do
- [ ] Add PowerShell Script to run from Windows Server
