# Connect Instance Pulumi

This repo contains code to deploy a simple Connect instance using Pulumi.

## One Time Setup

If this is you first time running Pulumi, ensure you chave completed the [relevant installations steps](https://www.pulumi.com/docs/install/)

After this login in the appropriate way. If just playing it is recommended to use the following, as it will use local setup and shouldn't require creating accounts or similar.

```bash
$ pulumi login --local
```

If required you may also need to set the active stack.

```bash
$ pulumi stack -s dev
```

## Modify Variables

The required variables are set in the `Pulumi.dev.yaml`, and can be editted there as required.

Alternately, these can also be modified by the command line using commands like the following:

```bash
$ pulumi config set connect-pulumi-deployment:namePrefix mynewprefix
$ pulumi config set aws:profile new-profile
```

## Create/Destroy

Once setup, and logged into the relevant AWS Profile, simply run the standard command

```bash
# To create
$ pulumi up
# To destroy
$ pulumi destroy
```
