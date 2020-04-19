# Notification gRPC

Notification gRPC is a services that handle notification communication with Email provider and Firebase via gRPC

## Installation

running locally: 
1. Make sure have at least python3 installed
2. Install dependency (pip install -r requirements.txt)
3. start services (make start-local)

running via container: 
1. Make sure have docker installed
2. Build image (make build)
3. Run image (make run)

## Usage

updating protos: 
1. Make sure all proto are valid
2. Build proto (make proto)

run unittest: 
unittest is configured to be run using pytest
1. all fixture can be found on conftest.py
2. run all unittest (pytest)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
