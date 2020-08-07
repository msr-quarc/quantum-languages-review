FROM  epiqc/scaffcc

ENV PATH "$PATH:/root/ScaffCC"

RUN apt-get update && apt-get install nano

# Copy projects over from the build context.
COPY *scaffold /root/src/
COPY Makefile /root/src/

WORKDIR /root/src/

# Commands below build teleport resource estimate and convert teletort circuit into OpenQASM
RUN cd /root/src && make
RUN cd /root/src && scaffold.sh -b teleport.scaffold

ENTRYPOINT [ "/bin/bash" ]