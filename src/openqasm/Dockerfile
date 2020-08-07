FROM conda/miniconda3:latest


# We need conda version 4.6 or later for shell integration.
RUN conda install 'conda>=4.6.0' -y

# Qiskit Terra requires gcc and cmake.
RUN apt-get update && \
    apt-get install -y gcc cmake

# We use a Conda environment specification to 
COPY environment.yml /root/environment.yml
RUN conda env create -f /root/environment.yml -p /env
RUN mkdir /src

# Qiskit Terra doesn't provide a way to directly run
# OpenQASM programs, so we copy over a small script to do so.
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
COPY *.py /src/

RUN useradd -ms /bin/bash quantum
USER quantum
RUN conda init bash && \
    echo 'conda activate /env' >> ~/.bashrc

COPY --chown=quantum:quantum *.qasm /src
# COPY --chown=quantum:quantum *.py /src

WORKDIR /src
ENTRYPOINT [ "/bin/bash" ]
