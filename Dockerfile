FROM frolvlad/alpine-python3
MAINTAINER Korwin Stevens

# Update apk
RUN apk update

# Install Python3 Dependencies
RUN pip3 install requests xlsxwriter datetime
