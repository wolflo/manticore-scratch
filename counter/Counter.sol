pragma solidity ^0.5.0;

contract Counter {
    uint256 public n;

    // manticore-verifier won't detect overflow over multiple txs
    // function inc() public { n++; }

    function add(uint val) public {
        // require(n + val >= n);
        n += val;
    }
}
