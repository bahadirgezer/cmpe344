# CMPE344 Labs

This repository contains the development environment and instructions for CMPE344 lab sessions. 

## Containerized Lab Environment for CMPE344

Containers provide the ability to package and run applications in a loosely isolated environment. We use container technology to package our development environment, where we install all required software and their dependencies. 

Docker was the first containerization platform and still is the most widely used software to manage containers. Check [Docker overview](https://docs.docker.com/get-started/overview/) for more information about Docker and containerization technology.

## Run the Lab Environment

### 1) Using Docker Engine

> :warning: You need [Docker Engine](https://docs.docker.com/engine/) installed on your system to proceed. You can install the engine for Ubuntu by following [installation steps](https://docs.docker.com/engine/install/ubuntu/). You can also follow [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/) to run `docker` without `sudo`.

> :warning: Windows users need to use Docker Desktop with WSL2 backend. See [the installation steps](https://docs.docker.com/desktop/install/windows-install/). 

You can pull the container using the command:
```
docker pull ghcr.io/bouncmpe/labs344
```

Then you can run the container using the command:
```
docker run -it --rm ghcr.io/bouncmpe/labs344
```


### 2) Using VSCode and Remote Containers extension

The code editor VSCode has an extension to allow you to develop inside containers called [Remote - Containers](https://code.visualstudio.com/docs/remote/containers). It will enable you to open any folder inside (or mounted into) a container and take advantage of VSCode fully. This project provides you with a `.devcontainer/devcontainer.json` file to configure the extension accordingly.

Once you have installed [Remote - Containers](https://code.visualstudio.com/docs/remote/containers) in the editor, you can open and work inside our lab environment using the extension.

## Getting started

The programs inside of this repository is runnable inside of the containerized lab environment. 

Use the Makefiles and whisper commands to try out the RISC-V programs.

### Labs:

1. [Fibonacci Numbers - Tutorial](./fibonacci/)

2. [Bubble Sort - First Lab](./bubble/)

3. [Coprime Array - Second Lab](./coprime/)
