# Proof of ID

### Summary
This contract allows you to create a unqiue identity on the blockchain. For now, this only works for individuals with a US social security number (SSN), but the idea can be generalized to any country and online identity database. The goal is to do this in a way that guarantees a person can only ever create one digital identity, such that they can receive a loan without collateral by proving that they never defaulted on one before, or participate in one-human-one-vote governance decisions on the blockchain.

The key difficulty is to compute your ID in a way that is unique to you throughout your life, while guaranteeing as much privacy as possible. These two features are at odds with each other, so we need to make trade-offs. 

Currently, the ID is computed in a way that allows anyone to check if it was created by someone with a certain name and birthday (it's not exactly, but _pretty much_ the same as directly revealing those details along with every ID). If they do that, they will also learn something (but not everything!) about the last 4 digits of your SSN: while there were 1000 possibilities for those 4 digits before, they can now narrow it down to around 300 possibilites. Right now, this information will be irreversably tied to the past and future transaction history of the Ethereum account that is used to create the ID. 

As we describe below however, the contract could be improved to provide better privacy: while you must still reveal personal info to create a unique digital identity, you can keep secret  _which_ personal details belong to a given unique identity on Ethereum.

### The big picture

### The contract
Your unique ID is computed from your personal info as follows:
```
ID = hash(name, birthday, ssn_bucket)
```
where `hash()` refers to [Ethereum's hash function](https://en.wikipedia.org/wiki/SHA-3) and all the inputs are verified by letting users log into their social security website at `https://secure.ssa.gov/RIL/` via an [Open Contracts enclave](https://opencontracts.io/#/protocol). I'll explain the `ssn_bucket` part in a second.

To understand how your ID works and what it does and doesn't reveal about you, I'll need to tell you how a [Hash function](https://en.wikipedia.org/wiki/Hash_function) works. Bear with me, it's important and won't be hard! :)

You can put any amount of data into a hash function, and it will always spit out what looks like a large random number (anywhere between 0 and 2^256). The same data always gives the same number, so it is not _really_ random, but if you change just one bit of the input data, the output changes unpredictably to some new number. This means that the output of a hash function has a special property: you cannot recover its inputs from the output, _except_ by trying out all possibilites until you guess the inputs _exactly_ right. 

Unfortunately, there are not that many possibile inputs for our ID, because there are not that many possible names, birthdays and last 4 SSN digits. So if we just put them all into a hash function and used it's output as ID, it would be easy for others to learn your last SSN digits by trying out all possible inputs and see which produce your ID, especially if they already know your name and birthday. But if we don't include the SSN digits, then IDs might not be unique because some people may share their name and birthday. Both would be problematic.

To solve this, we define 32 `ssn_bucket`s, each containing around 300 of the 10.000 possibilities of anyone's last 4 SSN digits. You can compute your `ssn_bucket` as follows:
```
ssn_bucket = hash(last 4 SSN digits) mod 32
```
where '[mod](https://en.wikipedia.org/wiki/Modulo_operation) 32' shortens the hash into a number between 0 and 31, which we call `ssn_bucket` and include in your ID. Since there are around 300 possibile last 4 SSN digits that fall into the same `ssn_bucket`, an attacker can only learn your name, birthday and bucket, but won't learn _that much_ about your SSN digits. But there's a way to improve privacy further, by keeping secret _which_ personal details belong to which Ethereum account.

### How to improve

If you are a developer, the first thing you could do is add more countries and identity databases.
But there's also an interesting way you could provide better privacy: using the ideas of [tornado.cash](https://tornado.cash), it is possible to disconnect a `personalID` that reveals a user's personal info (which we previously just called `ID`) from a separate `accountID` that users tie to their account. They would still only be able to create one of each, but others will not be able to tell which `accountID` belongs to which `personalID`. So users would publish some personal info to create a unique digital identity, but they would not reveal _which_ personal info was used to create _their_ digital identity.

Sounds like magic, but we can make it work using just enclaves and hash functions:
- 1] when verifying a user's `personalID`, the enclave also generates two random numbers called `accountID` and `secret` and computes `voucher=hash(accountID, secret)`.
- 2] the enclave tells the user their `accountID` and `secret`, and generates an oracle proof of `personalID` and `voucher`
- 3] the user publishes the oracle proof containing their `personalID` and `voucher`, that some stranger with an Ethereum account (who could be incentivzed via [OpenGSN](https://opengsn.org/)) will submit to the contract (so this submission does not reveal the user's Ethereum account).
- 4] if the oracle proof is valid and contains a new `personalID`, the contract appends `voucher` to a `voucherList`, and also updates ('puts it into') a state variable called `voucherUrn=hash(voucher, voucherUrn)`.
- 5] after a few days, a user could submit the `voucherList` to an enclave along with their `accountID` and `secret`, which computes their `voucher` and checks that it is in `voucherList`, then computes the most recent state of the `voucherUrn`, and gives the user an oracle proof for `voucherUrn` and `accountID` that they submit to the contract
- 6] if the submitted `voucherUrn` has a value that the `voucherUrn` in the contract had before, the user proves that their `accountID` is contained in a `voucher` that the contract previously put inside its `voucherUrn`, without revealing which one. This proves their `accountID` corresponds to a unique `personalID`, without revealing which one.



