# COOPER to Azure IoT Hub

[![Travis](https://img.shields.io/travis/hardwario/cp2azure/master.svg)](https://travis-ci.org/hardwario/cp2azure)
[![Release](https://img.shields.io/github/release/hardwario/cp2azure.svg)](https://github.com/hardwario/cp2azure/releases)
[![License](https://img.shields.io/github/license/hardwario/cp2azure.svg)](https://github.com/hardwario/cp2azure/blob/master/LICENSE)

## Installing

You can install **cp2azure** directly from PyPI:

```sh
sudo apt-get install libboost-python-dev
sudo pip3 install -U cp2azure
```

## Usage

Update config.yml and run

```sh
cp2azure -c config.yml
```

### Systemd

Insert this snippet to the file /lib/systemd/system/cp2azure.service:
```
[Unit]
Description=COOPER cp2azure
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/cp2azure -c /etc/cooper/cp2azure.yml
Restart=always
RestartSec=5
StartLimitIntervalSec=0

[Install]
WantedBy=multi-user.target
```

Start the service:

    sudo systemctl start cp2azure.service

Enable the service start on boot:

    sudo systemctl enable cp2azure.service

View the service log:

    journalctl -u cp2azure.service -f

## License

This project is licensed under the [**MIT License**](https://opensource.org/licenses/MIT/) - see the [**LICENSE**](LICENSE) file for details.
