# PhalaServerMonitor

This system has been designed to help manage Phala and Khala worker nodes.
The software gathers data like:
CPU Cores, Cpu temperature, Memory usage, phala service stats ....

The service then sends the  data to a backend server using a http post.
The default http endpoint is set to Cyber Jungle's servers. You can change
the endpoint my modifying the PhalaServiceUrl element in the config.json file.

This has been tested on Ubuntu 18.4.6.  It should run on later versions.


Installation:

Edit the config.json

Element Definitions:    
    PhalaServiceUrl: is the http endpoint for the data post. Default is the CyberJungle servers.
    CyberJunglePhalaAccount: This value is passed in the header as monitor_id. It is used to authenticate a server.
        You can generate an Account Id in the app.cyberjungle.io application.
    CyberJunglePhalaKey: This is a key used to secure communications to the server.  It's in the header
        as monitor_key.
    PhalaServicesBaseUrl: this is the base url for the phala services.  Normally this should be http://localhost
    UpdateInterval: the number of seconds between each polling.
    GasAccount:  This is the public address of the workers gas account.  This is used to get the amount of gas
        left in the account. 




run the install.sh shell script to install the required modules
./install.sh

To have the service start on boot run the install_autoboot.sh. This will copy the rc.local file to /etc and install the rc.local service.  If you already have rc.local installed, copy the content of the rc.local in this project and add it to the existion rc.local in /etc

./install_autoboot.sh


