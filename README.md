Metrics Exporter and Deployment using Ansible Role

This project involves a Python-based metrics exporter that collects system metrics (CPU, memory, disk, uptime, etc.) and exposes them in a Prometheus-compatible format. The deployment of this exporter script to remote Linux servers is automated using Ansible. The metrics are accessible on port 5000 via an HTTP endpoint for monitoring by Prometheus.

Prerequisites
Before running this Ansible role, ensure the following prerequisites are met:
Python Installed: Python must be installed on all target hosts.
Ansible Setup: Ansible must be installed and configured on the control node with privilege escalation (sudo) enabled.
Communication Established: Ensure SSH communication has been established with all remote nodes.
Inventory Configuration: Hosts must be predefined in /etc/ansible/hosts or in an inventory file defined in your working environment.

1. Steps to Deploy
Extract script into a folder e.g metrics_exporter

2. Configure Target Hosts
Set up your target hosts in the inventory file as shown above.

3. Running the Playbook
Once the prerequisites are met and the target hosts are configured, 
you can run the Ansible playbook to install the required Python libraries, copy the metrics_exporter.py script, and set up the service on the remote hosts. To run the playbook, use the following command:

ansible-playbook export_metrics.yml --ask-become-pass

This command will:
 i. Install the necessary Python libraries (psutil and prometheus_client) on the remote hosts using pip.
ii. Copy the metrics_exporter.py script to /usr/local/bin/ on the remote hosts.
iii. Create a systemd service to automatically run the script on the target machines.
iv. Enable and start the service so it begins exposing metrics.

4. Verify Service Status
After running the playbook, you can verify that the metrics_exporter service is running on the remote host by using the following command on the remote server:

systemctl status metrics_exporter