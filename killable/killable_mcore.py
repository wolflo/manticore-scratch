from manticore.ethereum import ManticoreEVM, ABI
m = ManticoreEVM()

saddr = m.make_symbolic_address()
user = m.create_account(balance=10**18, name='user')
killable = m.solidity_create_contract('Killable.sol', owner=user)

sval = m.make_symbolic_value(256)

killable.kill(sval, caller=user)

for st in m.ready_states:
    prop_killed = st.platform.transactions[-1].result == 'SELFDESTRUCT'
    if(prop_killed):
        st.constrain(prop_killed)
        [val] = st.solve_one_n(sval)
        print(f'contract self-destructed by kill( {val} )')
