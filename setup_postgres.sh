#!/bin/zsh

# Load environment variables from .env file
source passwords.env

# Check if the PostgreSQL server is already running
pg_ctl status -D "$PGDATA" > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "PostgreSQL server is already running."
else
  # Initialize the database directory
  initdb "$PGDATA"

  # Start the server
  pg_ctl -D "$PGDATA" -l logfile start

  # Wait for the server to start
  sleep 5
fi

# Create a user with the specified username and password
psql -d postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"

# Grant privileges to the user
psql -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

# Check if the database already exists
psql -d postgres -c "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1
if [ $? -eq 0 ]; then
  echo "Database '$DB_NAME' already exists."
else
  # Create the database with the specified name
  psql -d postgres -c "CREATE DATABASE $DB_NAME;"
fi


# Stop the server
#pg_ctl -D ./pgdata stop

# Run the server
# pg_ctl -D ./pgdata start

#brew services stop postgresql
