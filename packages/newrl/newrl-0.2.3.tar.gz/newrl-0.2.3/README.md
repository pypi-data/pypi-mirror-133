# newrl-py

## Installation
Add `newrl` to your project requirements 
and/or run the installation with:
```shell
pip install newrl
```


## Example usage

```python
    node = Node()

    balance = node.get_balance(
        'TOKEN_IN_WALLET', '0x16031ef543619a8569f0d7c3e73feb66114bf6a0', 10)
    print(balance)

    from newrl import generate_wallet_address
    wallet = generate_wallet_address()

    wallet_add_transaction = node.add_wallet(
        wallet['address'], '910', wallet['public'], 1)

    print(wallet_add_transaction)

    from newrl import sign_transaction

    signed_wallet_add_transaction = sign_transaction(
        wallet, wallet_add_transaction)
    print(signed_wallet_add_transaction)

    token_add_transaction = node.add_token(
        'my_new_token',
        '1',
        '0x16031ef543619a8569f0d7c3e73feb66114bf6a0',
        '0x16031ef543619a8569f0d7c3e73feb66114bf6a0',
        'fhdkfhldkhf',
        10000,
        10000,
    )

    signed_token_add_transaction = sign_transaction(
        wallet, token_add_transaction)
    print(signed_token_add_transaction)

    transfer_transaction = node.add_transfer(
        9, 10, '0x16031ef543619a8569f0d7c3e73feb66114bf6a0', '0x16031ef543619a8569f0d7c3e73feb66114bf6a0', 10, 10, 4)
    signed_transfer = sign_transaction(wallet, transfer_transaction)
    print(signed_transfer)

    validate_result = node.validate_transaction(signed_transfer)
    print(validate_result)

    print(node.run_updater())
```

