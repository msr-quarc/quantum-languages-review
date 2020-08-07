FROM haskell:8.8.3

RUN apt-get update && \
    apt-get install nano && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

# NB: cabal is per-user, so we need to drop permissions early.

RUN useradd -ms /bin/bash quantum
USER quantum
WORKDIR /home/quantum
RUN ghc --version && \
    cabal --version
RUN cabal v1-update && \
    # Note that we add the --max-backjumps argument based on the
    # advice at:
    #     https://www.mathstat.dal.ca/~selinger/quipper/README
    cabal v1-install quipper-all-0.9.0.0 --max-backjumps=10000

WORKDIR /src
COPY --chown=quantum:quantum *.hs /src/quipper-0.9/
COPY --chown=quantum:quantum Makefile /src/quipper-0.9/
COPY --chown=quantum:quantum build.sh /src/quipper-0.9/

WORKDIR /src/quipper-0.9/

# This builds and runs Teleport sample
RUN make

ENTRYPOINT [ "/bin/bash" ]
