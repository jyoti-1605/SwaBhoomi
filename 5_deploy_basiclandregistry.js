const BasicLandRegistry = artifacts.require("BasicLandRegistry");

module.exports = async function (deployer, network, accounts) {
  await deployer.deploy(BasicLandRegistry, {
    gas: 5500000,
    from: accounts[0]
  });
}; 