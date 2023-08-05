# ezcfn

A bootstrap for vanilla CloudFormation templating.

*ezcfn* is a CloudFormation bundling tool for keeping CloudFormation workflows
vanilla-flavoured.

*ezcfn* simplifies working with vanilla CloudFormation templates. It takes care
of building, gathering and distributing resource artifacts (such as
`Lambda Function` code, or `APIGateway` specifications), without altering
the development workflow when working with static interchange format
(*json* and *yaml*) templates.

*ezcfn* dissects and extends the existing functionalities of tools such as the
AWS CLI `cloudformation package` command.

Repository: [https://bitbucket.org/victorykit/ezcfn](https://bitbucket.org/victorykit/ezcfn)

Repository Mirror: [https://github.com/victoryk-it/ezcfn](https://github.com/victoryk-it/ezcfn)

# Get Started

```
python -m pip install ezcfn-victorykit
ezcfn --help
```

```
git clone git@bitbucket.org:victorykit/ezcfn-example.git
cd ezcfn-example
ezcfn resolve examples/nested/template.yaml \
    --s3-bucket mybucket \
    --s3-region eu-central-1 \
    --s3-prefix testd \
    --outdir ezcfn.out \
    --intrinsic
ls -al ezcfn.out/testd
```

## Documentation

The documentation can be found under [https://victorykit.bitbucket.io/ezcfn/](https://victorykit.bitbucket.io/ezcfn/).

## Licensing

Copyright (C) 2021  Tiara Rodney (victoryk.it)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <[https://www.gnu.org/licenses/](https://www.gnu.org/licenses/)>.

## More Information


* Architecture


* Contribution Guidelines
