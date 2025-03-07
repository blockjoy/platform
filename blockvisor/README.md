### Blockvisor

#### Prerequisites

- **bvup tool** (see assets below)
- **PROVISION_TOKEN** obtained from BlockJoy portal

#### OS Requirements

- Recommended: Ubuntu Server 18.04+
- Required: Linux kernel 5.10+

#### Install Dependencies

Besides standard Linux tools, Blockvisor requires the following CLI tools:
- pigz
- tar
- fallocate
- systemctl
- ip

```bash
apt update
apt install pigz util-linux e2fsprogs chrony
```

#### Install Apptainer

Required version: 1.3.0

See [Installing Apptainer](https://apptainer.org/docs/admin/main/installation.html). If you encounter issues, try building Apptainer from source.

#### Network Setup

Blockvisor uses Apptainer to run protocol nodes and requires a bridge interface. The default interface name is `bvbr0`. If using a different name, specify it when running `bvup` (see `bvup --help` for details).

##### Example Netplan Configuration

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp33s0:
      dhcp4: false
      dhcp6: false
  bridges:
    bvbr0:
      interfaces: [ enp33s0 ]
      addresses: [ 50.115.46.98/28 ]
      gateway4: 50.115.46.97
      nameservers:
        search: [ hosted.static.webnx.com ]
        addresses:
            - "1.1.1.1"
            - "8.8.8.8"
      parameters:
        stp: false
        forward-delay: 1
      dhcp4: no
      dhcp6: no
```

#### Apply Network Configuration

1. Apply netplan configuration: `netplan apply`
2. Verify that the bridge `bvbr0` is the primary interface
3. Reboot the server and verify the network configuration persists and the server is reachable

#### Host Provisioning with bvup

Once everything is configured, run bvup to provision the host and install Blockvisor:

```bash
./bvup <PROVISION_TOKEN> [--region REGION]
```

Where `<PROVISION_TOKEN>` is the token obtained from the BlockJoy portal.

See `bvup --help` for more details.

#### Verify Installation

After successfully running bvup:

1. Verify the config file is present at `/etc/blockvisor.json`
2. Check the service status:
   ```bash
   systemctl status blockvisor.service
   ```

#### Auto-update Configuration (Optional)

Blockvisor auto-update is enabled by default. To disable it:

1. Stop the Blockvisor service:
   ```bash
   bv stop
   ```

2. Modify `/etc/blockvisor.json` to include:
   ```json
   "update_check_interval_secs": null
   ```

3. Restart the service:
   ```bash
   bv start
   ```