# AWS Starter Kit

This kit uses [Stacker](http://stacker.readthedocs.io/en/latest/) to bootstrap a new AWS project.
The most important bits in here are the VPC networking, Bastion Host and Security Group setups.

More coming soon.

Prerequities:

- AWS Account with keys
- Docker
- SSH key file if setting up the Bastion host

The following environment variables need to be present in your shell:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

Usage:

- `cp conf/bz.env conf/$(whoami).env`
- Edit your conf file
- `make shell`
- `make build`
