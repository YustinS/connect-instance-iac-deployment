# High-Level Infrastructure-as-Code Look

This repo contains a high level look at a simplistic AWS deployment, orchestrated by some of the largest IaC tools in the market.

Note that Hashicorp CDKTF is excluded as it is still in pre-release status, however shares many similarities with the regular CDK, just with some specifics added.

## Terraform

As the core language personally used, this was pulled from a larger piece of work and used for comparison. Note that this source is actually a module, hence the slightly odd shape, however it works just as well directly worked with and adding variables.

As such it includes a few more configuration items than the others, however these are largely input variables that are directly applied, so could be replicated in the other, but as an educational task this didn't really add to the outcome.

## AWS CDK

Nothing too crazy about this, the biggest thing to note is the simplified number of resources due to the higher level constructs provided. This also includes a default S3 Access Policy restricting to HTTPS that the others don't include.

## Pulumi

A middle ground between CDK and Terraform, it shares a lot between the two other options.

The biggest thing you will run into here is having to go through multiple pages of documentation for the fundamental setup (finding how to configure input variables took awhile to track down), but once the core is setup adding resources feel very similar to Terraform, identifying the appropriate shape of the components.

## Pulumi Converted

Also included is the same Terraform configuration, converted into Pulumi using the built in CLI tooling.

This can be regenerated as required doing the following

```bash
$ cd ./connect-terraform-deployment
$ pulumi convert --from terraform --language python --out ../connect-terraform-pulumi-converted
```
