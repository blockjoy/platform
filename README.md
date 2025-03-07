# Blockvisor Stack

## Overview

The Blockvisor stack enables simple configuration, management, and replication of blockchain protocol deployments. It offers several key advantages:

- **Code-defined nodes** ensuring consistent and repeatable deployments
- **Resource isolation** by organizations, users, and nodes
- **Flexible deployment** options including private data centers and bare metal servers

## Architecture

The stack consists of four main components:

### 1. Blockvisor API

Centralized service that manages and provides access to all metadata and information about:
- Protocols
- Running nodes
- Host machines
- Users and organizations

### 2. Blockvisor

A daemon that runs on each host and communicates with the API either directly or through MQTT topics. It enables the management and coordination of nodes in the stack.

### 3. Blockvisor Protocols

Definitions imported into the API that specify:
- Node runtime parameters
- System requirements (memory, CPU, disk, firewall settings)
- Custom protocol configurations
- Additional custom applications that can run alongside protocol clients

### 4. Blockvisor Frontend

User interface for interacting with the API that provides:
- Node management
- Organization setup and user assignment
- Host onboarding information

## Deployment

### Blockvisor API

*Documentation coming soon*

### Blockvisor

Detailed documentation is available in the [blockvisor](blockvisor/README.md) directory.

#### High-Level Deployment Steps
- Download required bvup  and procure a token
- Install dependencies
- Install Apptainer
- Configure network
- Run bvup

## Blockvisor Protocol

Detailed documentation is available in the [blockvisor-protocols](blockvisor-protocols/README.md) directory.

### High-Level Development Steps
- Define protocol metadata in `babel.yaml`
- Define protocol clients
- Define protocol variants
- Publish protocol info to API
- Build and push protocol image to the registry
- Publish image to Blockvisor API


## Blockvisor Frontend

*Documentation coming soon*
