# Blockvisor Stack

## Overview

The Blockvisor stack enables simple configuration, management, and replication of blockchain protocol deployments. It offers several key advantages:

- **Code-defined nodes** ensuring consistent and repeatable deployments
- **Resource isolation** by organizations, users, and nodes
- **Flexible deployment** options including private data centers and bare metal servers

## Architecture
![BV Architecture](./blockvisor/overview.jpg)

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

### Quick Start Guide
#### Requirements
- docker
- docker compose
- git

### Quick Start Deployment
The following steps will deploy the Blockvisor stack in to a development ready environment.

1. Checkout the docs repo
> include all the submodules too
```bash
git clone --recurse-submodules https://github.com/blockjoy/blockvisor-docs.git
cd blockvisor-docs
```
2. Start the main stack 
> start and build all components
```bash
docker compose up --build -d
```

3. Initialize the database with Roles, Users and a dev Region
> This will create an initial admin user and non-admin user with the password you define
```bash
docker compose run init
```
```bash
[+] Creating 2/2
 ✔ Container blockvisor-docs-database-1  Running                                                                                                                                                                                                                                                                               0.0s
 ✔ Container blockvisor-docs-api-1       Running                                                                                                                                                                                                                                                                               0.0s
[+] Running 1/1
 ✔ Container blockvisor-docs-database-1  Healthy                                                                                                                                                                                                                                                                               0.5s

Enter your email: demo@example.com
Enter your first name: demo
Enter your last name: admin
Enter your password:

***Initial User Set is Complete***

----------Credentials----------
Admin User: 		demo@example.com
Non-Admin User: 	user@example.com
Both user passwords are set to what you defined.
The Blockvisor stack setup is complete.  You can now access it at http://<server_ip>
```

4. Stack setup is now complete.  Should now be able to login to the UI with the credentials you provided at the IP of your server or localhost.

![Login Page](./images/login.png "Login Page")

What have we installed?  This has deployed all the required services to run the blockvisor stack.  Including: blockvisor-api, blockvisor-web, a single blockvisor host, a postgres database, a local mqtt broker (emqx), the necessary proxies for the services, as well as an observability stack (prometheus, opentelemetry, loki, tempo, and grafana).

Some helpful links:
- UI: http://<server_ip>
- Grafana: http://<server_ip/grafana (admin/admin)
- EMQX UI: http://<server_ip>:18083 (admin/public)


:rotating_light: If you want to redeploy the blockvisor stack, you will need take the following steps :rotating_light:
1. Bring the stack down
```bash
docker compose down
```
2. Cleanup temp files
```bash
rm setup/success
```
3. Now you can redeploy a fresh stack.

### Next Steps

Great, so now you have the Blockvisor stack up and running and ready for testing and development.  The next items to consider:
1. Setup your local machine for development: [Link](./docs/blockvisor/bv_dev.md)
2. Building your own node image: [Link](https://github.com/blockjoy/blockvisor-protocols/blob/main/docs/HOWTO.md)
3. Publishing your protocol image to your API: [Link](https://github.com/blockjoy/blockvisor-protocols/blob/main/docs/HOWTO.md#testing-and-deploying-protocols)
4. Adding additional blockvisor hosts: [Link](https://github.com/blockjoy/bv-host-setup)

### Deep Dive

If you want to deep dive in to the code, how things work, or want more details you can checkout the documentation and code in each of the following repos for the four main components:

- Blockvisor API: [Link](https://github.com/blockjoy/blockvisor-api)
- Blockvisor Web App: [Link](https://github.com/blockjoy/blockvisor-app-web)
- Blockvisor Daemon: [Link](https://github.com/blockjoy/blockvisor)
- Blockvisor Protocols: [Link](https://github.com/blockjoy/blockvisor-protocols)
