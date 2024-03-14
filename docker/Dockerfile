FROM cae-artifactory.jpl.nasa.gov:17001/ubuntu:20.04
# FROM ubuntu:20.04

# comments here

ENV TZ 'America/Los_Angeles'

# Ubuntu packages

RUN echo $TZ > /etc/timezone && \
    apt-get update && apt-get install -y --no-install-recommends tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    dpkg --add-architecture i386 && apt-get update && \
    apt-get install -y --no-install-recommends less vim nano git curl make csh time python2 python3-pip python3-venv build-essential gcovr && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

RUN pip install Cheetah3==3.2.6
RUN pip install lxml==4.6.3
RUN pip install anytree==2.8.0

ENV PATH "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

ENTRYPOINT ["/bin/bash"]

ENV HOSTNAME "visar-container"
