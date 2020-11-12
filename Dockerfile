FROM python:3.8

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# install selenium
RUN pip install selenium
RUN apt-get update && apt-get install -y git 
RUN git clone https://github.com/galigutta/earn-date.git

WORKDIR /earn-date

RUN echo "#!/bin/bash" > startscript.sh
RUN echo "wget https://earn-dt.s3.amazonaws.com/et.csv" >> startscript.sh
RUN echo "git pull origin main" >> startscript.sh
RUN echo "head et.csv" >> startscript.sh
RUN chmod +x startscript.sh

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
RUN /opt/firefox/firefox -CreateProfile "headless /moz-headless"  -headless
#ADD user.js /moz-headless/

ENTRYPOINT ["sh","-c","./startscript.sh"]

#EXPOSE 4444

#ENTRYPOINT ["geckodriver"]

#CMD ["--binary=/opt/firefox/firefox", "--log=debug", "--host=0.0.0.0"]


