# BlockVisor CLI Administration Guide

The BlockVisor CLI tool (`bv`) is used to interact with the OS blockvisor component for blockchain node administration. This guide covers the basic usage and common commands for managing running nodes. 

The jobs, configurations, data folder structure, and content described in this guide are provisioned during node initialization based on RHAI script configurations. For information about initial protocol setup and RHAI configurations, please refer to the blockvisor-protocols guide.

## Basic Commands

### Checking BlockVisor Status

To check the status of the BlockVisor service:

```bash
bv status
```

This command shows the current status of the blockvisord service, including version, paths, and configuration.

Example output:
```
Service running: blockvisord 2.12.0 - Ok
 BV_PATH: /var/lib/blockvisor
 BABEL_PATH: /opt/blockvisor/2.12.0/blockvisor/bin/../../babel/bin/babel
 JOB_RUNNER_PATH: /opt/blockvisor/2.12.0/blockvisor/bin/../../babel/bin/babel_job_runner
 CONFIG: Config {
    id: "879303b0-4f9f-4628-8d6d-0c30da7bc917",
    private_org_id: None,
    name: "example.local",
    api_config: ApiConfig {
        token: "***",
        refresh_token: "***",
        blockjoy_api_url: "https://api.example.com",
    },
    blockjoy_mqtt_url: Some(
        "mqtts://mqtt.example.com:8883",
    ),
    update_check_interval_secs: Some(
        60,
    ),
    blockvisor_port: 9001,
    iface: "bvbr0",
    net_conf: NetConf {
        gateway_ip: 192.168.1.1,
        host_ip: 192.168.1.198,
        prefix: 24,
        available_ips: [
            192.168.1.199,
            192.168.1.200,
            192.168.1.201,
            192.168.1.202,
            192.168.1.203,
            192.168.1.204,
        ],
    },
    cluster_id: None,
    cluster_port: None,
    cluster_seed_urls: None,
    apptainer: ApptainerConfig {
        extra_args: None,
        host_network: false,
        cpu_limit: true,
        memory_limit: true,
    },
    maintenance_mode: false,
}
```

### Listing Nodes

To list all running nodes:

```bash
bv n ls
```

This command displays a table of all running nodes with their IDs, names, images, states, IP addresses, and uptime.

Example output:
```
----------------------------------------------------------------------------------------------------------------------------------------------
 ID                                    Name                       Image                                   State    IP Address      Uptime (s) 
 cb9e7769-8e44-4646-a89a-449ba00322f7  badly-curious-phoenix      optimism/op-reth-mainnet-archive/1.1.5  Running  192.168.1.199  710826     
 185a783b-e330-4f13-8bf1-97b42aa8a5c0  indirectly-destined-cobra  optimism/op-reth-mainnet-full/1.1.5     Running  192.168.1.200  710808     
 01bbe0d0-604c-4543-a4c0-a5456a09c003  briefly-clean-gator        ethereum/reth-mainnet-full/1.1.2        Running  192.168.1.201  205        
----------------------------------------------------------------------------------------------------------------------------------------------
```

### Getting Node Information

To get detailed information about a specific node:

```bash
bv n info <node-name>
```

This command provides detailed information about a specific node, including its configuration, status, and running jobs.

Example output:
```
Name:           indirectly-destined-cobra
Id:             185a783b-e330-4f13-8bf1-97b42aa8a5c0
Image:          NodeImage { id: "00000000-0000-0000-0000-000000000000", version: "1.1.5", config_id: "00000000-0000-0000-0000-000000000000", archive_id: "00000000-0000-0000-0000-000000000000", store_key: "dev-node-store-id", uri: "docker://ghcr.io/blockjoy/optimism-reth-protocol:v20250304.2", min_babel_version: "2.12.0" }
Status:         Running
Ip:             192.168.1.200
Gateway:        192.168.1.1
Uptime:         710821s
Protocol Status:     -
Block height:   -
Block age:      -
In consensus:   -
Jobs:
  - "op-node"
    Status:         Running
    Restarts:       1304
    Logs:
      2025-03-12 12:56:26.715392081 +00:00| Job 'op-node' finished with Ok(ExitStatus(unix_wait_status(256)))
      2025-03-12 12:55:20.638621810 +00:00| Job 'op-node' finished with Ok(ExitStatus(unix_wait_status(256)))
      2025-03-12 12:54:14.041077120 +00:00| Job 'op-node' finished with Ok(ExitStatus(unix_wait_status(256)))
      2025-03-12 12:53:08.289230583 +00:00| Job 'op-node' finished with Ok(ExitStatus(unix_wait_status(256)))
      2025-03-12 12:52:02.005674081 +00:00| Job 'op-node' finished with Ok(ExitStatus(unix_wait_status(256)))
      2025-03-12 12:50:55.934523835 +00:00| Job 'op-node' finished with Ok(ExitStatus(unix_wait_status(256)))
      ... use `bv node job info op-node` to get more
  - "caddy"
    Status:         Running
    Restarts:       0
  - "init_job"
    Status:         Finished with exit code 0
    Restarts:       0
  - "alloy"
    Status:         Running
    Restarts:       0
  - "grafana"
    Status:         Running
    Restarts:       0
  - "op-reth"
    Status:         Running
    Restarts:       0
Requirements:   cpu: 0, memory: 32768MB, disk: 1000GB
Assigned CPUs:  []
Tags:  []
```

### Restarting Nodes

To restart a specific node:

```bash
bv n restart <node-name>
```

This command will stop and then start the specified node. All jobs associated with the node will be restarted.

Example output:
```
Stopped node `01bbe0d0-604c-4543-a4c0-a5456a09c003`
Started node `01bbe0d0-604c-4543-a4c0-a5456a09c003`
```

### Managing Node Jobs

List all jobs for a specific node:

```bash
bv n job <node-name> ls
```

Example output:
```
NAME                           STATUS
caddy                          Running
grafana                        Running
op-reth                        Running
alloy                          Running
op-node                        Running
init_job                       Finished with exit code 0
```

Get information about a specific job:

```bash
bv n job <node-name> info <job-name>
```

Example output:
```
status:           Running
restart_count:    0
upgrade_blocking: false
logs:             <empty>
```

View the logs of a specific job:

```bash
bv n job <node-name> logs -f <job-name>
```

Example output:
```
2025-03-10T09:08:30.258713Z  INFO reth::cli: Starting reth version="1.2.0 (1e965ca)"
2025-03-10T09:08:30.258737Z  INFO reth::cli: Opening database path="/blockjoy/protocol_data/optimism/op-reth/db"
2025-03-10T09:08:30.334596Z  INFO reth::cli: Launching node
2025-03-10T09:08:30.339463Z  INFO reth::cli: Configuration loaded path="/blockjoy/protocol_data/optimism/op-reth/reth.toml"
2025-03-10T09:08:30.344928Z  INFO reth::cli: Verifying storage consistency.
2025-03-10T09:08:30.346368Z  INFO reth::cli: Database opened
2025-03-10T09:08:30.346376Z  INFO reth::cli: Starting metrics endpoint at 127.0.0.1:6060
```

Note: The `-f` flag follows the log output in real-time, similar to `tail -f`.

### Starting and Stopping Jobs

Individual jobs within a node can be stopped and started:

```bash
bv n job <node-name> stop <job-name>   # Stop a specific job
bv n job <node-name> start <job-name>  # Start a stopped job
```

Example:
```bash
bv n job briefly-clean-gator stop grafana   # Stop the Grafana service
bv n job briefly-clean-gator start grafana  # Start the Grafana service
```

### Container Management with Apptainer

BlockVisor uses Apptainer to run lightweight containers for each node. You can interact with these containers directly using Apptainer commands.

List all running container instances:

```bash
apptainer instance list
```

Example output:
```
INSTANCE NAME                           PID        IP                IMAGE
01bbe0d0-604c-4543-a4c0-a5456a09c003    4043845    192.168.1.201    /var/lib/blockvisor/nodes/01bbe0d0-604c-4543-a4c0-a5456a09c003/rootfs
185a783b-e330-4f13-8bf1-97b42aa8a5c0    1401978    192.168.1.200    /var/lib/blockvisor/nodes/185a783b-e330-4f13-8bf1-97b42aa8a5c0/rootfs
cb9e7769-8e44-4646-a89a-449ba00322f7    1400608    192.168.1.199    /var/lib/blockvisor/nodes/cb9e7769-8e44-4646-a89a-449ba00322f7/rootfs
```

View resource usage statistics for a specific instance:

```bash
apptainer instance stats <instance-name>
```

Example output:
```
INFO:    Stats for 185a783b-e330-4f13-8bf1-97b42aa8a5c0 instance of /var/lib/blockvisor/nodes/185a783b-e330-4f13-8bf1-97b42aa8a5c0/rootfs (PID=1401978)

INSTANCE NAME                           CPU USAGE    MEM USAGE / LIMIT      MEM %    BLOCK I/O            PIDS
185a783b-e330-4f13-8bf1-97b42aa8a5c0    0.84%        369.5MiB / 30.52GiB    1.18%    912KiB / 7.662GiB    387
```

This provides insights into the container's resource consumption, including CPU usage, memory utilization, I/O operations, and the number of processes.

### System Logs

BlockVisor logs can be viewed using the system journal. To view the logs in real-time:

```bash
journalctl -t blockvisor -fn 50
```

This command shows the last 50 lines of BlockVisor logs and follows new entries. The logs include important information such as:
- MQTT connection status
- Job status changes and restarts
- Error messages and warnings

Example output:
```
Mar 12 13:11:37 example.local blockvisor[3599344]: MQTT incoming = PingResp(PingResp)
Mar 12 13:11:37 example.local blockvisor[3599344]: MQTT watch wait...
Mar 12 13:11:50 example.local blockvisor[3599344]: id: cb9e7769-8e44-4646-a89a-449ba00322f7; declared: 1000000000000; actual: 4296127111
Mar 12 13:11:50 example.local blockvisor[3599344]: id: 185a783b-e330-4f13-8bf1-97b42aa8a5c0; declared: 1000000000000; actual: 4296128430
Mar 12 13:11:50 example.local blockvisor[3599344]: id: 01bbe0d0-604c-4543-a4c0-a5456a09c003; declared: 2000000000000; actual: 25946436979
Mar 12 13:11:52 example.local blockvisor[3599344]: No metrics collected
Mar 12 13:11:54 example.local blockvisor[1402495]: Job 'op-node' finished with Ok(ExitStatus(unix_wait_status(256)))  - retry
Mar 12 13:11:54 example.local blockvisor[1402495]: Spawned job 'op-node'
Mar 12 13:11:56 example.local blockvisor[1401033]: Job 'op-node' finished with Ok(ExitStatus(unix_wait_status(256)))  - retry
Mar 12 13:11:56 example.local blockvisor[1401033]: Spawned job 'op-node'
```

Common log entries to watch for:
- Job restart messages: Indicate when jobs are being restarted, possibly due to failures
- MQTT messages: Indicate the status of the connection to the BlockJoy API
- Error messages: Help identify issues with nodes or jobs

## Directory Structure

BlockVisor organizes its files and nodes in a specific directory structure under `/var/lib/blockvisor/`. Here's an overview of the important directories and files:

### Root Directory (`/var/lib/blockvisor/`)

```
/var/lib/blockvisor/
├── commands_cache.pb      # Command cache file
├── downloads/             # Downloaded resources
└── nodes/                 # Contains all node instances
    ├── state.json         # Global nodes state
    └── <node-id>/         # Individual node directories
```

### Node Directory Structure

Each node has its own directory named with its UUID. Here's the structure of a node directory (`/var/lib/blockvisor/nodes/<node-id>/`):

```
<node-id>/
├── apptainer.pid           # Process ID file
├── cgroups.toml            # CGroups configuration
├── data/                   # Node-specific data
├── rootfs/                 # Container root filesystem
│   ├── blockjoy/           # BlockJoy specific files
│   ├── var/lib/babel/jobs/ # Job-specific directories
│   │   ├── alloy/          # Alloy job files
│   │   ├── caddy/          # Caddy job files
│   │   ├── create_jwt/     # JWT creation job files
│   │   ├── grafana/        # Grafana job files
│   │   ├── lighthouse/     # Lighthouse job files
│   │   └── reth/           # Reth job files
│   │       ├── config.json # Job configuration
│   │       └── logs        # Job log files
│   └── ...                 # Standard Linux filesystem structure
└── state.json              # Node state information
```

### Node Data Directory

The `data/` directory in each node's folder contains persistent data for the node's services:

```
data/
├── .protocol_data.lock   # Lock file for protocol data
├── caddy/                # Caddy server data
└── protocol_data/        # Protocol-specific data
    ├── lighthouse/       # Lighthouse client data
    └── reth/             # Reth client data
```

This directory stores the blockchain data, client databases, and other persistent information needed by the node's services. Each protocol component (like Lighthouse and Reth) maintains its own data directory to ensure data isolation and proper management.

### Job Directories

Each job in the node has its own directory under `/var/lib/blockvisor/nodes/<node-id>/rootfs/var/lib/babel/jobs/` containing:
- `config.json`: Job-specific configuration
- `logs`: Job log files

This structure allows for organized management of multiple nodes and their associated jobs, with each component having its own isolated space for configuration and data.
