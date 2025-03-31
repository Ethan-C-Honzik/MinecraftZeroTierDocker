FROM ghcr.io/graalvm/graalvm-ce:ol8-java17-22.3.3 

WORKDIR /app

# Install Bash using microdnf
RUN microdnf update -y && \
    microdnf install -y python3 && \
    microdnf clean all

STOPSIGNAL SIGTERM