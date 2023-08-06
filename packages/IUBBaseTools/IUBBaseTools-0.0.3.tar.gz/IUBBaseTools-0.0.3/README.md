# IUB Base tool
IUB Base Tool contains a set of base class used for IUB scripts

## Contained tools
Here a list of the contained tools:
* **IUBConfiguration**: used to read yaml settings from a file
* **FTPUploader**: used to upload files inside a directory to cloud
* **Locker**: check if another instance of the requested script is already running
* **TorrentHandler**: send requests to the server that is controlling Transmission
* **UploadDb**: store data to a text file as plaintext
* **ApiHandler**: set of API used to communicate with IUB server

## Build guide
To release a new build:
1. Edit the `setup.cfg` file setting the correct version
2. 