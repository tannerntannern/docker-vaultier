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

#### Problems with the Original
Vaultier is awesome software, but unforunately, the [official project](http://www.vaultier.org/) is no longer maintained and installing it is tiresome with little to no help online.  The official site's documentation and installation links appear to be broken, except for the Docker one.  Even though the Docker image appears to "work", emails don't send properly and the data doesn't persist if you stop the Docker container.

#### The Solution
Luckily for you, I went through all the hassle of building my own Docker image based on the official [rclick/vaultier](https://hub.docker.com/r/rclick/vaultier/) image that patches the holes you get with it out of the box.

## Installation
#### Requirements
  - A Linux-based OS (all my testing was done on Ubuntu 16.04)
  - [Docker](https://www.docker.com/) (here's an [installation guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04) for Ubuntu 16.04)
  
#### Setup
First, you'll want to pull the [Docker image](https://hub.docker.com/r/tannerntannern/vaultier/) from the [Docker Hub](https://hub.docker.com/):

```
sudo docker pull tannerntannern/vaultier:latest
```

Next, you'll want to make a directory for Vaultier to hold all its data.  **This step is important** as Docker containers do not retain any data after they stop running.  The folder will be shared by the Docker container so that your data persists even if you stop and restart the container.  The location does not matter, but the 777 permissions are necessary.

```
sudo mkdir -m 777 /my/vaultier/storage/folder
```

#### Running the Application
Once you have the image and storage folder setup, you can try running the application with the following command (the parts you can change are double-bracketed):

```
sudo docker run \
    --name vaultier \
    -p 8888:80 \
    --rm \
    -d \
    -v /my/vaultier/storage/folder:/vaultier_data \
    tannerntannern/vaultier:latest
```

After it starts up, the app will be accessible at [localhost:8888](localhost:8888).  To stop the app, run the following command:

```
sudo docker stop vaultier
```

## Configuration
Coming soon...

## Caveats
Coming soon...
