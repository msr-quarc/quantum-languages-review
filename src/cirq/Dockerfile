FROM conda/miniconda3:latest

# Cirq depends on LaTeX, so we need to install it first.
RUN apt-get update && apt-get install -y texlive-base latexmk

# We need conda version 4.6 or later for shell integration.
RUN conda install 'conda>=4.6.0' -y

# We use a Conda environment specification to 
COPY environment.yml /root/environment.yml
RUN conda env create -f /root/environment.yml -p /env
RUN mkdir /src

RUN useradd -ms /bin/bash quantum
USER quantum
RUN conda init bash && \
    echo 'conda activate /env' >> ~/.bashrc

COPY --chown=quantum:quantum *.py /src/

WORKDIR /src
ENTRYPOINT [ "/bin/bash" ]
