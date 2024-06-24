#!/bin/bash

# MySQL credentials
MYSQL_USER=root
MYSQL_PASSWORD=root_password

# Create a temporary SQL script file
SQL_SCRIPT=$(mktemp)

# Write the SQL commands to the temporary script file
cat <<EOF > $SQL_SCRIPT
-- Create database hbnb_test_db if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create user hbnb_test with password hbnb_test_pwd if it doesn't exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on hbnb_test_db to hbnb_test
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema to hbnb_test
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
EOF

# Execute the SQL script
mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" < $SQL_SCRIPT

# Remove the temporary SQL script file
rm $SQL_SCRIPT

echo "MySQL setup completed."
