FROM ubuntu:22.04 AS builder

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UT
ENV RUST_VERSION=1.83.0

RUN apt-get update && \
    apt-get install -y git software-properties-common gpg psmisc ufw pigz tar util-linux e2fsprogs chrony wget jq curl build-essential pkg-config libssl-dev cmake musl-tools unzip

RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v30.1/protoc-30.1-linux-x86_64.zip && \
    unzip protoc-30.1-linux-x86_64.zip && \
    mv ./bin/protoc /usr/bin/ && \
    mv ./include/* /usr/include/
RUN protoc --version
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain ${RUST_VERSION} && \
    . "$HOME/.cargo/env" && \
    rustup default ${RUST_VERSION} && \
    rustup target add x86_64-unknown-linux-gnu

RUN git clone https://github.com/blockjoy/blockvisor.git
RUN cd blockvisor && \
    . "$HOME/.cargo/env" && \
    export PATH="$PATH:/usr/local/include" && \
    git config --file .gitmodules submodule.proto.url https://github.com/blockjoy/api-proto.git && \
    git config --file .gitmodules submodule.proto.path bv/proto && \
    git submodule sync && \
    git submodule update --init --recursive && \
    make build-release
RUN cd blockvisor && \
    mkdir -p /tmp/bundle/blockvisor/bin /tmp/bundle/blockvisor/services && \
    cp target/x86_64-unknown-linux-musl/release/bv /tmp/bundle/blockvisor/bin && \
    cp target/x86_64-unknown-linux-musl/release/blockvisord /tmp/bundle/blockvisor/bin && \
    cp target/x86_64-unknown-linux-musl/release/installer /tmp/bundle && \
    cp bv/data/blockvisor.service /tmp/bundle/blockvisor/services && \
    cp target/x86_64-unknown-linux-musl/release/nib /tmp/bundle/blockvisor/bin && \
    mkdir -p /tmp/bundle/babel/bin && \
    cp target/x86_64-unknown-linux-musl/release/babel /tmp/bundle/babel/bin && \
    cp target/x86_64-unknown-linux-musl/release/babel_job_runner /tmp/bundle/babel/bin && \
    cp target/x86_64-unknown-linux-musl/release/bvup /tmp/bvup && \
    mkdir /tmp/bundle/docs && \
    cp babel_api/rhai_plugin_guide.md /tmp/bundle/docs && \
    cp -r babel_api/examples /tmp/bundle/docs && \
    mkdir /tmp/bundle/sh_complete && \
    cp target/x86_64-unknown-linux-musl/release/sh_complete/_bv /tmp/bundle/sh_complete/ && \
    cp target/x86_64-unknown-linux-musl/release/sh_complete/bv.bash /tmp/bundle/sh_complete/ && \
    cp target/x86_64-unknown-linux-musl/release/sh_complete/_nib /tmp/bundle/sh_complete/ && \
    cp target/x86_64-unknown-linux-musl/release/sh_complete/nib.bash /tmp/bundle/sh_complete/

FROM ubuntu:22.04

WORKDIR /app

ENV RUST_LOG=info,blockvisor=debug,babel=debug,bv_utils=debug
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get update
RUN add-apt-repository -y ppa:apptainer/ppa
RUN apt-get install -y apptainer gpg psmisc ufw pigz tar util-linux e2fsprogs chrony wget jq
RUN mkdir /opt/blockvisor

COPY ./init.sh .
RUN chmod +x ./init.sh 
COPY --from=builder /tmp/bundle /opt/blockvisor
COPY --from=builder /tmp/bvup /usr/local/bin/

CMD ["./init.sh"]
