const LandRegistry = artifacts.require("LandRegistry");

module.exports = async function (deployer, network, accounts) {
  await deployer.deploy(LandRegistry, accounts[0]); // ✅ pass the deployer address
}; 