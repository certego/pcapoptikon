# PCAPOptikon
PCAPOptikon is a project that will provide a web GUI and some REST APIs to analyze arbitrary PCAP files with Suricata IDS.

PCAPOptikon uses Django 1.8 and TastyPie.

## Docker image
Docker is surely the quickest way to get started with PCAPOptikon. You can download it by running:

    $ sudo docker pull pdelsante/pcapoptikon

Now, I would suggest you to create a _data-only_ docker container to grant the persistence of MySQL data (`pdelsante/pcapoptikon` exposes the volume `/var/lib/mysql`):

    $ sudo docker create --name pcapoptikon_data pdelsante/pcapoptikon

Now, a couple other directories that you may want to create locally on your host are:

    $ mkdir -p /var/log/pcapoptikon
    $ mkdir -p /var/tmp/pcapoptikon

You can then run your docker container this way:

    $ sudo docker run -d --name=pcapoptikon --volumes-from=pcapoptikon_data -v=/var/log/pcapoptikon:/var/log -v=/var/tmp/pcapoptikon:/var/tmp -p=8000:8000 pdelsante/pcapoptikon

This command will create a new daemonized docker container, called `pcapoptikon`, mounting `/var/lib/mysql` from `pcapoptikon_data` and mounting `/var/log` and `/var/tmp` from the folders you just created on the host. It will also expose the container's port 8000 on localhost, so that you can simply point your browser to: http://localhost:8000/

Default username and password are `admin:admin`. You will find some useful info on your host's `/var/log/pcapoptikon/pcapoptikon_startup.log` and in the other log files in the same folder.

Should you own a valid ETPro oinkcode, you can supply it to the startup script that way:

    $ sudo docker run -d --name=pcapoptikon --volumes-from=pcapoptikon_data -v=/var/log/pcapoptikon:/var/log -v=/var/tmp/pcapoptikon:/var/tmp -p=8000:8000 pdelsante/pcapoptikon /opt/pcapoptikon/start.sh <your_oinkcode_here>

Please note that, in this last case, you have to specify the docker instance's entry point `/opt/pcapoptikon/start.sh` yourself.

## Manual Install

### System-wide requirements
Please make sure the following packages are installed:

    $ apt-get install mysql-server mysql-common mysql-client libmysqlclient-dev python-dev

PCAPOptikon needs a Suricata instance running on the same host as the rest of the program. Installing it is pretty simple:

    $ sudo apt-get install software-properties-common python-software-properties
    $ sudo add-apt-repository -y ppa:oisf/suricata-stable
    $ sudo apt-get update
    $ sudo apt-get install suricata

PCAPOptikon expects to find `classification.config` and `reference` under the folder `/etc/suricata/rules/` instead than just `/etc/suricata/` (which is the default), so please make sure that your `/etc/suricata/suricata.yaml` contains the following:

    classification-file: /etc/suricata/rules/classification.config
    reference-file: /etc/suricata/rules/reference.config

It is also recommended that you install `oinkmaster` (or `pulledpork`) and configure it as appropriate (rule url, oinkcode, etc).

You may also want to enable the following option in `/etc/suricata/suricata.yaml`:

    - rule-reload: true

Doing so will let Suricata reload the rules whenever you send the process a `SIGUSR2` signal, without having to restart it. So, for example, you can run the following:

    $ oinkmaster -C /etc/oinkmaster.conf -o /etc/suricata/rules && killall -SIGUSR2 suricata

If you're using the `./start.sh` script which comes with PCAPOptikon, it will do that for you.

### Python requirements
First of all, this will clone PCAPOptikon in your current working directory:

    $ git clone https://github.com/pdelsante/pcapoptikon.git

**Please consider using VirtualEnv, especially if you already have other projects running on Django versions other than 1.8**. Installing VirtualEnv is extremely easy:

    $ sudo pip install virtualenv

Actually, you only need sudo if you're installing `virtualenv` globally (which I suggest you to do). Now, `cd` to PCAPOptikon's root directory to create and activate your virtual environment:

    $ cd pcapoptikon
    $ virtualenv venv
    $ source venv/bin/activate

That's all. The first command will create a folder named `venv`, with a copy of the Python executable, pip and some other tools; the second command will activate the virtual environment for you. From now on, every time you run `pip install`, the requested modules will be installed locally, without touching your global Python environment.

Now make sure that the virtual environment is still active and then install the requirements by running:

    $ pip install -r requirements.txt

Now, use pip to copy the `suricatasc` module from your system-wide python install:

    $ pip install --no-index --find-links=/usr/lib/pymodules/python2.7/ suricatasc

Now you're ready to install PCAPOptikon itself. First, please create a new empty MySQL database and populate it:

    $ mysqladmin create pcapoptikon
    $ python manage.py migrate

You are now ready to create a new user by running:

    $ python manage.py createsuperuser

## Running PCAPOptikon
Launch the daemon with the following command (from PCAPOptikon's root directory):

    $ python manage.py run_daemon

Now, you can run the web GUI with the following:

    $ python manage.py runserver

By default, this will run the server on 127.0.0.1:8000 (you will only be able to reach it from localhost). If you wish to reach it from the local network, simply run:

    $ python manage.py runserver 0.0.0.0:8000

or whatever other port you want.

## Using PCAPOptikon

### The GUI
Simply point your browser to http://127.0.0.1:8000/ (or whatever ip/port you chose) and enjoy a simple web GUI that lets you submit new tasks and show their results.

### The Admin GUI
PCAPOptikon includes a standard Django admin GUI that will help you manage your tasks (you can delete or modify them from there): http://127.0.0.1:8000/admin/

### The APIs
PCAPOptikon also includes a full REST API made with `django-tastypie`. To access it programatically, it's recommended that you use an API key. You can create one via the Admin GUI (see above).

The API endpoint can be found at http://127.0.0.1:8000/api/v1/?format=json

To list all the pending tasks, just visit: http://127.0.0.1:8000/api/v1/task/?format=json

To view the status of task #1: http://127.0.0.1:8000/api/v1/task/1/?format=json

Making a POST request to http://127.0.0.1:8000/api/v1/task/ will create a new task for you. Please note that the PCAP file you're sending will need to be encoded with base64. An example Python script making a POST request to create a new task is the following:

    import base64
    import json
    import os
    import requests
    
    
    api_url     = "http://127.0.0.1:8000/api/v1/"
    api_user    = "<YOUR_API_USER_HERE>"
    api_key     = "<YOUR_API_KEY_HERE>"
    pcap_file   = "/path/to/dump.pcap"
    
    headers = {
        'Authorization': 'ApiKey {}:{}'.format(api_user, api_key),
        'Content-Type': 'application/json'
    }
    
    with open(pcap_file, 'rb') as i:
        payload = {
            'pcap_file': {
                "name": os.path.basename(self.pcap_path),
                "file": base64.b64encode(i.read()),
                "content_type": "application/vnd.tcpdump.pcap",
            }
        }
    
    response = requests.post(
        os.path.join(api_url, 'task/'),
        data=json.dumps(payload),
        headers=headers
    )
    
    if response.status_code == 201:
        retrieve_url = response.headers['Location']
        log.debug("Will need to poll URL: {}".format(retrieve_url))
    
        # Now you can start polling the address specified by retrieve_url
        # to retrieve the results, which will be available in a few seconds.
    else:
        # Something went wrong
        raise Exception("Got status code: {}".format(response.status_code))
