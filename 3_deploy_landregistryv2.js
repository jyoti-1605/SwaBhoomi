const LandRegistryV2 = artifacts.require("LandRegistryV2");

module.exports = async function (deployer, network, accounts) {
  await deployer.deploy(LandRegistryV2, {
    gas: 5500000,
    from: accounts[0]
  });
}; 