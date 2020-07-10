pragma solidity ^0.5.0;

import "./Counter.sol";

// manticore-verifier CounterProperties.sol --contract CounterProperties
contract CounterProperties is Counter {
    constructor() public {
        n = 1;
    }
    function crytic_overflow() public returns (bool) {
        return n >= 1;
    }
}
