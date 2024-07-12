#!/usr/bin/python3
"""
Fabric script to deploy an archive to web servers.
"""
import os
from fabric import task, Connection
from datetime import datetime

# Define the web server IPs
env.hosts = ['<IP web-01>', '<IP web-02>']


@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to web servers and deploys it.

    Args:
    - c (object): Fabric connection context.
    - archive_path (str): Local path to the archive to deploy.

    Returns:
    - bool: True if deployment was successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        print(f"Archive file '{archive_path}' does not exist.")
        return False

    try:
        # Upload the archive to /tmp/ directory on the web servers
        archive_name = os.path.basename(archive_path)
        tmp_archive_path = f"/tmp/{archive_name}"
        c.put(archive_path, tmp_archive_path)

        # Extract archive to /data/web_static/releases/
        # <archive_filename_without_extension>/
        archive_folder = archive_name.replace('.tgz',
                                              '').replace('.tar.gz', '')
        remote_release_path = f"/data/web_static/releases/{archive_folder}"
        c.run(f"mkdir -p {remote_release_path}")
        c.run(f"tar -xzf {tmp_archive_path} -C {remote_release_path}")

        # Delete the archive from the web servers
        c.run(f"rm {tmp_archive_path}")

        # Delete the current symbolic link
        c.run("rm -rf /data/web_static/current")

        # Create a new symbolic link pointing to the deployed archive
        c.run(f"ln -s {remote_release_path} /data/web_static/current")

        print("New version deployed successfully!")
        return True

    except Exception as e:
        print(f"Error deploying: {e}")
        return False
