from manticore.ethereum import ManticoreEVM
from manticore.core.plugin import Plugin
from manticore.utils import config
m = ManticoreEVM()

# gas is serious
consts_evm = config.get_group("evm")
consts_evm.oog = "pedantic"

# print gas cost of each CALL instruction, including any returned stipend
class CheckCallGas(Plugin):
    prestate_gas = 0
    def will_evm_execute_instruction_callback(self, state, op, args):
        if op.semantics == 'CALL':
            self.prestate_gas = state.platform.current_vm.gas

    def did_evm_execute_instruction_callback(self, state, op, args, result):
        if op.semantics == 'CALL':
            vm = state.platform.current_vm
            print(f'call from {hex(vm.address)} to {hex(args[1])}')
            print(f'value: {args[2]}')
            print(f'gas consumed: {self.prestate_gas - vm.gas}')

m.register_plugin(CheckCallGas())

# loads an address from calldata, then calls to that address with msg.value
caller_code = bytes.fromhex('60008080803481355af100')
calling_contract = m.create_account(code=caller_code)

user = m.create_account(balance=10000000)
existing_acct = m.create_account(balance=1, nonce=1, code=bytes.fromhex('00'))
new_acct_address = 111111111111111111111111111111111111111111111111

print(f'user: {hex(user.address)}')
print(f'existing account: {hex(existing_acct.address)}')
print(f'non-existant account: {hex(new_acct_address)}')

def int_to_address(value):
    return b'\x00' * 12 + bytes.fromhex(hex(value)[2:])

# consumes 32400 gas
# 700 base + 9000 + 25000 - 2300 returned stipend
# expected cost 700 + 9000 - 2300 = 7400
print('\ncall to existing account with value\n----------')
m.transaction(caller=user,
              address=calling_contract,
              value=1,
              data=int_to_address(existing_acct.address))

# consumes 25700 gas
# 700 base + 25000
# expected cost 700
print('\ncall to non-existant account without value\n----------')
m.transaction(caller=user,
              address=calling_contract,
              value=0,
              data=int_to_address(new_acct_address))

# correctly consumes 700 gas
print('\ncall to existing account without value\n----------')
m.transaction(caller=user,
              address=calling_contract,
              value=0,
              data=int_to_address(existing_acct.address))
