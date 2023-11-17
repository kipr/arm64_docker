# Use the official Debian base image for ARM64 architecture
FROM debian:bullseye

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Utilities
RUN apt-get update && apt-get install -q -y --no-install-recommends \
    build-essential \
    cmake \
    dirmngr \
    git \
    gnupg2 \
    nano \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Update the package list and install the required packages
RUN apt-get update && apt-get install -y \
    doxygen \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN echo "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d

# Set the default command to run when the container starts (e.g., a shell)
CMD ["/bin/bash"]
