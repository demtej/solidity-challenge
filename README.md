## Index
  - [Assumptions and constraints](#assumptions-and-constraints)
  - [About the proposed solution](#about-the-proposed-solution)
	  - [PoolDeposit](#pool-deposit)
	  - [PoolRewards](#pool-rewards)
  - [How EthPool calculate the total of an account?](#How-EthPool-calculate-the-total-of-an-account?)
  
 [**Rinkeby Link**](https://rinkeby.etherscan.io/address/0xa6b978624F4Dc1C464A93772e798f0331Fd4F477#code)

##  Assumptions and constraints

  

- From the "challenge readme" I assume that any rewards deposits without any pool deposit lead to inaccessible funds so the proposed solution block it.

- The proposed solution supports rewards deposits for any period.

  

##  About the proposed solution

* Credits [Scalable Reward Distribution on the Ethereum
Blockchain](http://batog.info/papers/scalable-reward-distribution.pdf)

## Installation 

* Credits [@PatrickAlphaC](https://github.com/PatrickAlphaC)

Prerequisites

Please install or have installed the following:

- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.


```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
# restart your terminal
pipx install eth-brownie
```
Or, if that doesn't work, via pip
```bash
pip install eth-brownie
```

## Testnet Development
If you want to be able to deploy to testnets, do the following. 

### With environment variables

Set your `WEB3_INFURA_PROJECT_ID`, and `PRIVATE_KEY` [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html). 

You can get a `WEB3_INFURA_PROJECT_ID` by getting a free trial of [Infura](https://infura.io/). At the moment, it does need to be infura with brownie. If you get lost, you can [follow this guide](https://ethereumico.io/knowledge-base/infura-api-key-guide/) to getting a project key. You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.io/). 

You'll also need testnet rinkeby ETH and LINK. You can get LINK and ETH into your wallet by using the [rinkeby faucets located here](https://docs.chain.link/docs/link-token-contracts#rinkeby). If you're new to this, [watch this video.](https://www.youtube.com/watch?v=P7FX_1PePX0)

You can add your environment variables to the `.env` file:

```
export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
export PRIVATE_KEY=<PRIVATE_KEY>
export PRIVATE_KEY_B=<PRIVATE_KEY_B> //to work with 2 accounts
```

AND THEN RUN `source .env` TO ACTIVATE THE ENV VARIABLES
(You'll need to do this everytime you open a new terminal, or [learn how to set them easier](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html))

> DO NOT SEND YOUR PRIVATE KEY WITH FUNDS IN IT ONTO GITHUB

## Local Development

For local testing [install ganache-cli](https://www.npmjs.com/package/ganache-cli)
```bash
npm install -g ganache-cli
```
or
```bash
yarn add global ganache-cli
```

All the scripts are designed to work locally or on a testnet. You can add a ganache-cli or ganache UI chain like so: 
```
brownie networks add Ethereum ganache host=http://localhost:8545 chainid=1337
```
And update the brownie config accordingly. There is a `deploy_mocks` script that will launch and deploy mock Oracles, VRFCoordinators, Link Tokens, and Price Feeds on a Local Blockchain. 


## Deploy to a testnet / Scripts

```
brownie run scripts/deploy.py
```

To run the unit tests:
```
brownie test
```





