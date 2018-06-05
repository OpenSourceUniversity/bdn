
# Blockchain Delivery Node



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* `Make sure you have a copy of the OSUNI platform project on your local machine.`
* `Docker installed`

### Installing

Create project directory and execute the following command in order to clone the project:

    git clone https://git.codeideo.com/edu-ico/platform.git

### Running

## Increase the VM max map count

    docker-machine ssh
    sudo sysctl -w vm.max_map_count=262144
    exit

Within the project directory execute the following commands:

    docker-compose up
    docker-compose run web python manage.py migrate

Open your browser on this address and you will be able so see django administration page: http://localhost:8000/

To setup local user for administration panel execute:

    docker-compose run web python manage.py createsuperuser

In OSUni platform directory execute:

    rm -R build
    truffle migrate (with Ganache/Test RPC working).

    After successful compilation copy from OSUni platform directory - ./build/contracts/* to ./bdn/contracts/*

In BDN project folder run

    docker-compose run web python manage.py certificate_syncer

## Running the tests

To simulate certificates adding in OSUni platform directory execute

    truffle exec scripts/faker.js

    To be added other tests.

### Coding style

Make sure the style of the source code you commit is consistent with the style of the rest of the project.

## Deployment

To be added.

## Built With

* [web3.py](https://github.com/ethereum/web3.py) - A python interface for interacting with the Ethereum blockchain and ecosystem
* [django](https://www.djangoproject.com/) - Development framework for web applications

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **RECHAINED** - *Initial work* - [RECHAINED](https://rechained.com)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
