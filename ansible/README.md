# Ansible Playbooks for K8s Security Guardian

This directory contains Ansible playbooks for preparing bare-metal nodes for Kubernetes deployment with security hardening.

## Usage

1. **Configure Inventory**
   Edit `inventory.ini` with your node IP addresses and SSH credentials.

2. **Run Preparation Playbook**
   ```bash
   ansible-playbook -i inventory.ini playbook.yml
   ```

## What the playbook does:

- Disables SWAP (required for kubelet)
- Loads and persists br_netfilter kernel module
- Configures sysctl parameters for Kubernetes networking
- Installs Docker container runtime
- Installs Kubernetes components (kubelet, kubeadm, kubectl)
- Holds package versions to prevent accidental upgrades

## Security Features:

- Uses `become: yes` for privileged operations
- Configures secure networking defaults
- Installs only necessary packages
- Holds Kubernetes packages to maintain version consistency