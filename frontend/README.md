# Coffee Shop Frontend

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing Ionic Cli

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, run:

```bash
npm install
```
> _Note_: Upgrading to new version of the dependencies might prevent the project from running, as it depends on the specific version listed in ```package.json```


## Running Your Frontend

The application is then accessible through the browser on a localhost port. To run the server, cd into the `frontend` directory and run:

```bash
ionic serve
```