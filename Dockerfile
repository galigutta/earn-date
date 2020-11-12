# https://hub.docker.com/_/debian
FROM debian:buster-slim

ARG firefox_ver=82.0.2
ARG geckodriver_ver=0.28.0

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends --no-install-suggests \
            ca-certificates \
 && update-ca-certificates \
    \
 # Install tools for building
 && toolDeps=" \
        curl bzip2 \
    " \
 && apt-get install -y --no-install-recommends --no-install-suggests \
            $toolDeps \
    \
 # Install dependencies for Firefox
 && apt-get install -y --no-install-recommends --no-install-suggests \
            `apt-cache depends firefox-esr | awk '/Depends:/{print$2}'` \
            # additional 'firefox-esl' dependencies which is not in 'depends' list
            libxt6 \
    \
 # Download and install Firefox
 && curl -fL -o /tmp/firefox.tar.bz2 \
         https://ftp.mozilla.org/pub/firefox/releases/${firefox_ver}/linux-x86_64/en-GB/firefox-${firefox_ver}.tar.bz2 \
 && tar -xjf /tmp/firefox.tar.bz2 -C /tmp/ \
 && mv /tmp/firefox /opt/firefox \
    \
 # Download and install geckodriver
 && curl -fL -o /tmp/geckodriver.tar.gz \
         https://github.com/mozilla/geckodriver/releases/download/v${geckodriver_ver}/geckodriver-v${geckodriver_ver}-linux64.tar.gz \
 && tar -xzf /tmp/geckodriver.tar.gz -C /tmp/ \
 && chmod +x /tmp/geckodriver \
 && mv /tmp/geckodriver /usr/local/bin/ \
    \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
            $toolDeps \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/* \
 && apt-get update \
 && apt-get install -y python3 python3-pip wget \
 && pip3 install lxml==4.6.1 beautifulsoup4==4.9.3 bs4==0.0.1 soupsieve==2.0.1 numpy==1.19.4 pandas==1.1.4 python-dateutil==2.8.1 pytz==2020.4 \
 && pip3 install certifi==2020.11.8 chardet==3.0.4 edgar==5.4.1 fuzzywuzzy==0.18.0 idna==2.10 python-levenshtein==0.12.0 requests==2.25.0 tqdm==4.51.0 urllib3==1.26.1

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

ENTRYPOINT ["sh","-c","./startscript.sh"]

#EXPOSE 4444

#ENTRYPOINT ["geckodriver"]

#CMD ["--binary=/opt/firefox/firefox", "--log=debug", "--host=0.0.0.0"]


