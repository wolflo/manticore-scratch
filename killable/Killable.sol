pragma solidity ^0.5.0;

contract Killable {

    function kill(uint val) external {
        if(val > 0 && val % 2 == 0) {
            selfdestruct(msg.sender);
        }
    }

}
