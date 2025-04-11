const SimpleLandRegistry = artifacts.require("SimpleLandRegistry");

module.exports = async function (deployer, network, accounts) {
  await deployer.deploy(SimpleLandRegistry, {
    gas: 5500000,
    from: accounts[0]
  });
}; 