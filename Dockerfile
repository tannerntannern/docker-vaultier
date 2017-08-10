FROM rclick/vaultier:latest

# Required packages
RUN sudo apt-get update && \
    sudo apt-get install rsync -y --fix-missing

# Connect to folder provided by host machine
VOLUME /vaultier_data
RUN chmod ugo+w /vaultier_data

# Override mailing behavior
ADD ./mailer.py /opt/vaultier/venv/lib/python2.7/site-packages/vaultier/vaultier/business/mailer.py
ADD ./send_mail_examples /opt/vaultier/send_mail_examples

# Override supervisord configuration
ADD ./supervisord.conf /etc/supervisor/supervisord.conf

# Make sure postgresql uses the shared host volume for storage (continued in start.sh)
RUN service postgresql stop && \
    sed -i "/data_directory = /c\data_directory = '/vaultier_data/database/postgresql/9.3/main'" /etc/postgresql/9.3/main/postgresql.conf

# Run script on start
ADD ./start.sh /opt/vaultier/start.sh
ENTRYPOINT ["/opt/vaultier/start.sh"]