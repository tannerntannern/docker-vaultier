# Vaultier for Docker :whale:
> An awesome, free, secure, key-based, multi-user, self-hosted password manager for teams.

## Introduction
Need a password manager for your team?  Vaultier is a great choice if you want a password manager that is:
  - **Free to use**
  - Multi-user
  - Self-hosted
  - Simple to setup
  - Open source

Note that this is more or less a **"turn-key" solution**.  You can choose where to store the database and how to send emails, but if you want more customization, you'd be better off forking this or the official repository and implementing the changes yourself.

If this all sounds good to you, then keep reading!

### Problems with the Original
Vaultier is awesome software, but unforunately, the [official project](http://www.vaultier.org/) is no longer maintained and installing it is tiresome with little to no help online.  The official site's documentation and installation links appear to be broken, except for the Docker one.  Even though the Docker image appears to "work", emails don't send properly and the data doesn't persist if you stop the Docker container.

### The Solution
Luckily for you, I went through all the hassle of building my own Docker image based on the official [rclick/vaultier](https://hub.docker.com/r/rclick/vaultier/) image that patches the holes you get with it out of the box.  By using my image you'll be able to:
  - Easily keep your database files persistent
  - Have emails delivered the way you want them to be

## Getting Started
### System Requirements
  - Linux-based OS (all my testing was done on Ubuntu 16.04)
  - [Docker](https://www.docker.com/) (here's an [installation guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04) for Ubuntu 16.04)
  
### Installation
First, you'll want to pull the [Docker image](https://hub.docker.com/r/tannerntannern/vaultier/) from the [Docker Hub](https://hub.docker.com/):

```
sudo docker pull tannerntannern/vaultier:latest
```

Next, you'll want to make a directory for Vaultier to hold all its data.  **This step is important** as Docker containers do not retain any data after they stop running.  The folder will be shared by the Docker container so that your data persists even if you stop and restart the container.  The location does not matter, but the 777 permissions are necessary.

```
sudo mkdir -m 777 /my/vaultier/storage/folder
```

### Running the Application
Once you have the image and storage folder setup, you can try running the application with the following command:

```
sudo docker run \
    --name vaultier \
    -p 8888:80 \
    --rm \
    -d \
    -v /my/vaultier/storage/folder:/vaultier_data \
    -e "VAULTIER_DOMAIN=localhost" \
    tannerntannern/vaultier:latest
```

After it starts up, the app will be accessible at [http://localhost:8888](http://localhost:8888).  A few things to note here:
  - **VAULTIER_DOMAIN must be set to the domain that you plan to host with for others to access the app.**  If you plan to host internally or without a domain name, an IP address will suffice.  
  - Be sure to put the actual storage folder you chose earlier in place of "/my/vaultier/storage/folder"
  - Emails won't send properly quite yet; see the Email Configuration section below to set it up

If everything worked properly, you should also see a new **database** folder and **scripts** folder in the storage folder you chose earlier.

### Stopping the Application
To stop the app, run the following command:

```
sudo docker stop vaultier
```

## Email Configuration
Emails were a big issue in the original application (at least, for me).  They still aren't perfect in my version, but you have the huge benefit of
  - customizing exactly how your emails get sent
  - seeing when and what went wrong (if anything does)
  - and having a complete log of all sent (or attempted) emails.

### How it Works
After Vaultier has run for the first time, you will see something like the following in the **scripts** directory inside the storage folder you chose earlier:

```
scripts
├── send_mail_examples
│   ├── send_mail.generic_template.py
│   ├── send_mail.mailgun.py
│   └── send_mail.mailtrap.py
└── send_mail.py
```

When Vaultier starts up, it looks in this directory and copies the `send_mail.py` script to be used internally.  Inside `send_mail.py` should be a function called `send_mail(from_email, to_emails, subject, plain_body, html_body)` that **you must implement yourself**.  The `send_mail_examples` folder has a few default implementations, such as [Mailtrap](https://mailtrap.io/) and [Mailgun](https://www.mailgun.com/), as well as a generic template to get you started with making your own.

**NOTE:**  *If you make changes to `send_mail.py`, be sure to stop and restart the Vaultier container, as the script only gets loaded when the container starts up.*

### Email Logs
Since Vaultier is more or less running inside a "black box," I setup Vaultier to log information to **email.log** and **email_errors.log**, both of which are in the root of the storage folder you chose earlier.

#### email.log
This log contains copies of every single email that gets sent by Vaultier.  If you don't feel like getting emails to send properly with Vaultier, you could simply dig through this file to get the information you need.  (Not recommended, but possible)

#### email_errors.log
This log contains any errors that happened as a result of `send_mail.py`, which is useful for debugging your send_mail implementation.

## Authors
The original [Vaultier](http://www.vaultier.org) project was developed by [RightClick](http://startups.rclick.cz/).

This particular adaptation of the project was developed by **Tanner Nielsen**.
