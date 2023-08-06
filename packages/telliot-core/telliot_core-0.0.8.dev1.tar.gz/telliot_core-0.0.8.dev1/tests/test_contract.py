"""
Test covering Pytelliot EVM contract connection utils.
"""
import pytest
import web3
from web3 import Web3

from telliot_core.apps.core import TelliotCore
from telliot_core.contract.gas import fetch_gas_price
from telliot_core.queries.legacy_query import LegacyRequest


@pytest.mark.asyncio
async def test_connect_to_tellor(rinkeby_cfg):
    """Contract object should access Tellor functions"""
    async with TelliotCore(config=rinkeby_cfg) as core:
        assert len(core.tellorx.master.contract.all_functions()) > 0
        assert isinstance(
            core.tellorx.master.contract.all_functions()[0],
            web3.contract.ContractFunction,
        )


@pytest.mark.asyncio
async def test_call_read_function(rinkeby_cfg):
    """Contract object should be able to call arbitrary contract read function"""

    async with TelliotCore(config=rinkeby_cfg) as core:
        (reward, tips), status = await core.tellorx.oracle.read(
            func_name="getCurrentReward",
            _queryId="0x0000000000000000000000000000000000000000000000000000000000000001",
        )
        assert status.ok
        assert reward >= 0


@pytest.mark.skip(reason="oracle contract does not have faucet right now")
@pytest.mark.asyncio
async def test_faucet(rinkeby_cfg):
    """Contract call to mint to an account with the contract faucet"""
    # estimate gas
    gas_price = await fetch_gas_price()
    # set up user
    async with TelliotCore(config=rinkeby_cfg) as core:

        user = core.tellorx.master.node.web3.eth.account.from_key(
            core.get_default_staker().private_key
        ).address
        # read balance
        balance1, status = await core.tellorx.master.read(
            func_name="balanceOf", _user=user
        )
        assert status.ok
        assert balance1 >= 0
        print(balance1)
        # mint tokens to user
        receipt, status = await core.tellorx.master.write_with_retry(
            func_name="setBalanceTest",
            gas_limit=350000,
            gas_price=gas_price,
            extra_gas_price=20,
            retries=1,
            _address=user,
            _amount=1e18,
        )
        assert status.ok
        # read balance again
        balance2, status = await core.tellorx.master.read(
            func_name="balanceOf", _user=user
        )
        assert status.ok
        print(balance2)
        assert balance2 - balance1 == 1e21


@pytest.mark.skip("Move to end-to-end tests")
@pytest.mark.asyncio
async def test_trb_transfer(rinkeby_cfg):
    """Test TRB transfer through TellorMaster contract (and its proxies)"""

    async with TelliotCore(config=rinkeby_cfg) as core:

        gas_price = await fetch_gas_price()
        sender = core.tellorx.master.node.web3.eth.account.from_key(
            core.config.main.private_key
        ).address
        balance, status = await core.tellorx.master.read("balanceOf", _user=sender)
        print("my sender address:", sender)
        print("my sender balance:", balance / 1e18)
        recipient = str(
            Web3.toChecksumAddress("0xf3428C75CAfb3FBA46D3E190B7539Fbbfb96f244")
        )

        balance, status = await core.tellorx.master.read("balanceOf", _user=recipient)
        assert status.ok
        print("before:", balance / 1e18)

        receipt, status = await core.tellorx.master.write_with_retry(
            "transfer",
            _to=recipient,
            _amount=1,
            gas_limit=350000,
            gas_price=gas_price,
            extra_gas_price=20,
            retries=2,
        )
        print(status.error)
        assert status.ok

        balance, status = await core.tellorx.master.read("balanceOf", _user=recipient)
        print("after:", balance / 1e18)


@pytest.mark.skip("Move to end-to-end tests")
@pytest.mark.asyncio
async def test_submit_value(rinkeby_cfg):
    """E2E test for submitting a value to rinkeby"""

    async with TelliotCore(config=rinkeby_cfg) as core:

        gas_price_gwei = await fetch_gas_price()
        user = core.tellorx.master.node.web3.eth.account.from_key(
            core.config.main.private_key
        ).address
        print(user)

        balance, status = await core.tellorx.master.read("balanceOf", _user=user)
        print(balance / 1e18)

        is_staked, status = await core.tellorx.master.read(
            "getStakerInfo", _staker=user
        )
        print(is_staked)

        if is_staked[0] == 0:
            _, status = await core.tellorx.master.write_with_retry(
                func_name="depositStake",
                gas_limit=350000,
                gas_price=gas_price_gwei,
                extra_gas_price=20,
                retries=2,
            )
            assert status.ok

        q = LegacyRequest(legacy_id=99)
        value = q.value_type.encode(420.0)

        query_data = q.query_data
        query_id = q.query_id

        timestamp_count, status = await core.tellorx.oracle.read(
            func_name="getTimestampCountById", _queryId=query_id
        )
        assert status.ok
        assert timestamp_count >= 0
        print(timestamp_count)

        receipt, status = await core.tellorx.oracle.write_with_retry(
            func_name="submitValue",
            gas_limit=350000,
            gas_price=gas_price_gwei,
            extra_gas_price=40,
            retries=5,
            _queryId=query_id,
            _value=value,
            _nonce=timestamp_count,
            _queryData=query_data,
        )

        print(status.error)
        assert status.ok
