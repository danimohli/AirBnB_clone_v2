#!/usr/bin/python3
"""
archive from the contents of the web_static
"""
from fabric import task
from datetime import datetime
import os


@task
def do_pack(c):
    """
    Creates a .tgz archive from the contents of the web_static folder.
    """
    try:
        # Generate timestamp
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_name = f'web_static_{now}.tgz'

        # Create versions directory if it doesn't exist
        c.run('mkdir -p versions')

        # Create .tgz archive
        c.run(f'tar -cvzf versions/{archive_name} web_static')

        archive_path = os.path.join('versions', archive_name)

        # Check if archive was created successfully
        if c.exists(archive_path):
            return archive_path
        else:
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
