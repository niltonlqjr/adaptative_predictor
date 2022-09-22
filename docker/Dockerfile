# Ubuntu dependencies
FROM ubuntu:20.04
# FROM nvidia/cuda:11.2.0-runtime-ubuntu20.04

ARG USER_ID
ARG GROUP_ID

RUN apt-get update -y && apt-get install -y locales gnupg curl sudo \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8


# YaCos System Dependencies
RUN curl https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - \
    && echo "deb http://apt.llvm.org/focal/ llvm-toolchain-focal-10 main" | tee -a /etc/apt/sources.list \
    && apt-get update -y

RUN DEBIAN_FRONTEND="noninteractive" TZ="America/Sao_Paulo" \
    apt-get install -y graphviz libgraphviz-dev creduce libeigen3-dev linux-tools-generic bc \
    clang-10 clang-format-10 libclang1-10 libclang-10-dev libclang-common-10-dev \
    wget python3 python3-dev python3-pip python3-virtualenv python3-setuptools \
    python3-ipython python-is-python3 gcc g++ cmake make binutils git tar zip unzip


RUN update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-10 100 \
    && update-alternatives --install /usr/bin/clang clang /usr/bin/clang-10 100 \
    && update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-10 100 \
    && update-alternatives --install /usr/bin/opt opt /usr/bin/opt-10 100 \
    && update-alternatives --install /usr/bin/llvm-link llvm-link /usr/bin/llvm-link-10 100 \
    && update-alternatives --install /usr/bin/llc llc /usr/bin/llc-10 100 
    #&& rm /usr/bin/perf \
    #&& update-alternatives --install /usr/bin/perf perf /usr/lib/linux-tools/5.4.0-125-generic/perf 100


RUN wget https://github.com/sharkdp/hyperfine/releases/download/v1.11.0/hyperfine_1.11.0_amd64.deb \
    && dpkg -i hyperfine_1.11.0_amd64.deb && rm -f hyperfine_1.11.0_amd64.deb

RUN pip3 install tensorflow \
    && pip3 install tensorboard \
    && pip3 install protobuf \ 
    && pip3 install cython
# YaCos IR2VEC Dependencies
RUN git clone https://github.com/IITH-Compilers/IR2Vec.git \
    && mkdir -p IR2Vec/build && cd IR2Vec/ \
    && git checkout llvm10 \
    && cd build \
    && cmake -DLT_LLVM_INSTALL_DIR=/usr -DEigen3_DIR=/usr -DCMAKE_INSTALL_PREFIX=/usr ../src \
    && make install \
    && cd ../.. \
    && rm /usr/seedEmbeddingVocab-300-llvm10.txt \
    && rm -rf IR2Vec


# Creating and switching to a non-root user and the group 
RUN addgroup --gid $GROUP_ID nonroot \
    && adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID nonroot \
    && usermod -aG sudo nonroot \
    && echo "nonroot ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers
#RUN useradd --create-home --gid sudo --shell /bin/bash --system nonroot \
#    && echo "nonroot ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers

USER nonroot
WORKDIR /home/nonroot
ENV LANG en_US.utf8


# Insalling YaCoS Data
RUN mkdir -p /home/nonroot/.local/yacos \
    && wget --progress=bar:force:noscroll www.csl.uem.br/repository/yacos/yacos_data.tar.xz \
    && tar xfJ yacos_data.tar.xz -C $HOME/.local/yacos \
    && rm -f yacos_data.tar.xz \
    && wget --progress=bar:force:noscroll www.csl.uem.br/repository/yacos/yacos_tests.tar.xz \
    && tar xfJ yacos_tests.tar.xz -C $HOME/.local/yacos \
    && rm -f yacos_tests.tar.xz

## Copying and installing YaCos
RUN git clone https://github.com/ComputerSystemsLaboratory/YaCoS.git
RUN sudo chown --recursive nonroot /home/nonroot/YaCoS \
    && chmod --recursive 777 /home/nonroot/YaCoS
RUN cd /home/nonroot/YaCoS/cython_lbpeq \
    && sudo python3 setup.py install \
    && sudo rm -rf cythonlbpeq.egg-info \
    && sudo rm -rf build \
    && sudo rm -rf dist
RUN cd /home/nonroot/YaCoS/ && sudo python3 setup.py build
RUN cd /home/nonroot/YaCoS/ && sudo python3 setup.py install
