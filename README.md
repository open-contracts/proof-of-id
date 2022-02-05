# Proof of ID

### Summary
This contract allows you to create a unqiue identity on the blockchain. For now, this only works for individuals with a US social security number (SSN), but the idea can be generalized to any country and online identity database. The goal is to do this in a way that guarantees a person can only ever prove ownership of one ID in their life, such that they can accrue a credit history that incentivizes them to repay loans without collateral, or participate in one-human-one-vote governance decisions on the blockchain.

The key difficulty is to compute your ID in a way that is unique to you throughout your life, while guaranteeing as much privacy as possible. These two features are at odds with each other, so we need to make trade-offs. 

Currently, the ID is computed in a way that allows anyone to check if it was created by someone with a certain name and birthday (it's not exactly, but _pretty much_ the same as directly revealing those details along with every ID). If they do that, they will also learn something (but not everything!) about the last 4 digits of your SSN: while there were 1000 possibilities for those 4 digits before, they now narrowed it down to around 300 possibilites (which you can [compute here](https://colab.research.google.com/drive/1uEs2eUB8_uG7i_-X1nCds_8wQ_3Ue2JL?usp=sharing)). Right now, this information will be irreversably tied to the past and future transaction history of the Ethereum account that is used to create the ID. 

As we describe below howver, the contract could be improved to provide much better privacy: by publishing your ID _without_ tying it to your Ethereum account right away.

### The big picture

### The contract
Your unique ID is computed from your personal info as follows:
```
ID = hash(first name,
          last name,
          birthday,
          hash(last 4 SSN digits) mod 32)
```
where `hash()` refers to [Ethereum's hash function](https://en.wikipedia.org/wiki/SHA-3) and all the inputs are verified by letting users log into their social security website at `https://secure.ssa.gov/RIL/` via an [Open Contracts enclave](https://opencontracts.io/#/protocol). I'll explain the `mod 32` part in a second.

To understand how your ID works and what it does and doesn't reveal about you, I'll need to tell you how a [Hash function](https://en.wikipedia.org/wiki/Hash_function) works. Bear with me, it's important and won't be hard! :)

You can put any amount of data into a hash function, and it will always spit out what looks like a large random number (anywhere between 0 and 2^256). The same data always gives the same number, so it is not _really_ random, but if you change just one bit of the input data, the output changes unpredictably to some new number. This means our ID has a unique property: you cannot recover the personal info from the ID, _except_ by trying out all possibilites until you guess the inputs _exactly_ right. 



### How to improve

If you are a developer, here's how you could improve the contract to provide better privacy: using the ideas of [tornado.cash](https://tornado.cash), it is possible to disconnect a `personalID` that reveals a user's personal info (which we previously just called `ID`) from a separate `accountID` that users tie to their account. They would still only be able to create one `accountID`, but others will not be able to tell which `accountID` belongs to which `personalID`. Here's how the magic works:
- 1] when verifying their `personalID`, the enclave also generates two random numbers called `accountID` and `secret` and computes `voucher=hash(accountID, secret)`.
- 2] the enclave tells the user their `accountID` and `secret`, and generates an oracle proof of `personalID` and `voucher`
- 3] the user publishes the oracle proof containing their `personalID` and `voucher`, that some volunteer with an Ethereum account (who could be incentivzed via [OpenGSN](https://opengsn.org/)) will submit to the contract.
- 4] if the oracle proof is valid and contains a new `personalID`, the contract appends `voucher` to a `voucherList`, and updates a state variable called `root=hash(voucher, root)`.
- 5] after a few days, a user could submit the `voucherList` to an enclave along with their `accountID` and `secret`, which computes `voucher` and checks that it is in `voucherList`, then computes `root`, and gives the user an oracle proof containing `root` and `accountID` they submit to the contract via their Ethereum account 
- 6] if the submitted `root` is equal to one that the contract computed before, it connects `accountID` to the user's account.



