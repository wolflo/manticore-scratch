from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators as Props
m = ManticoreEVM()

ETH = 10**18
user = m.create_account(balance=1*ETH, name='user')
counter = m.solidity_create_contract('Counter.sol',
                                     contract_name='Counter',
                                     owner=user)

# generate symbolic initial state and argument
sval0 = m.make_symbolic_value(256)
sval1 = m.make_symbolic_value(256)

# set initial state
for st in m.ready_states:
    st.platform.set_storage_data(counter, 0, sval0)

# call add() with symbolic argument
counter.add(sval1)

# check if an overflow is possible
for st in m.ready_states:
    n = st.platform.get_storage_data(counter, 0)
    prop_overflow = Props.ULT(n, sval0)

    # if an overflow is possible, generate a concrete case that triggers it
    if st.can_be_true(prop_overflow):
        st.constrain(prop_overflow)
        val0, val1 = st.solve_one_n(sval0, sval1)
        print('shit')
        print(f'overflow!\ninitial value: {val0}\ncall: add({val1})')
