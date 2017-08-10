#!/usr/bin/env bash

# Make storage folders if they aren't present
DB_DIR="/vaultier_data/database"
SCRIPT_DIR="/vaultier_data/scripts"
mkdir -m 777 ${DB_DIR} ${SCRIPT_DIR}

# Copy database files over if they don't exist
if [ "$(ls -A $DB_DIR)" ]
then
    echo "Using existing database.";
else
    echo "Setting up database files for the first time...";

    # Replicate database data on the host
    rsync -av /var/lib/postgresql ${DB_DIR}

    # Remove unused data
    rm -rf /var/lib/postgresql/9.3/main
fi

# Copy send_mail scripts over if the script directory is empty
if [ "$(ls -A $SCRIPT_DIR)" ]
then
    echo "Using existing scripts"
else
    echo "Setting up script files for the first time...";

    # Copy example scripts over
    mv /opt/vaultier/send_mail_examples ${SCRIPT_DIR}/send_mail_examples
fi

# Pull out the mailtrap example code if send_mail doesn't exist
if [ ! -f "$SCRIPT_DIR/send_mail.py" ]
then
    cp ${SCRIPT_DIR}/send_mail_examples/send_mail.mailtrap.py ${SCRIPT_DIR}/send_mail.py
fi

# Copy user-made send_mail script so that vaultier can use it
cp ${SCRIPT_DIR}/send_mail.py /opt/vaultier/venv/lib/python2.7/site-packages/vaultier/vaultier/business/

# Let supervisord take control from now on
exec /usr/bin/supervisord
