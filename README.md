# Proof of Legacy Identity





The current implementation has a major privacy issue, which can be split into two aspects: 
 1) Your ID basically reveals your name, birthday and last SSN digit, because a [Preimage Attack](https://en.wikipedia.org/wiki/Preimage_attack) is definitely feasible. That's why we're not using all last 4 digits, even though it would make IDs more unique.
 2) Your ID _is_ the unique digital identity that gets linked to your Ethereum account (so anyone who knows your ID can find your transaction history). It would be much better if the former only has to be published when creating a one-time _voucher_, which can later be used up to create a unique identity for your Ethereum account, without revealing which voucher was used.

Number 2) should be solvable by literally copying the source code of [TornadoCash](https://github.com/tornadocash). Logic: 
- user submits a `secret` to the enclave, which submits `voucher=hash(secret)` along with the ID, and can only do so if ID wasn't submitted yet.
- contract aggregates all vouchers into a single merkle tree
- a while later, a user can create their actual unique digital identity by producing a zero-knowledge proof that they know a secret that hashes to a voucher contained in the merkle tree, without revealing which one.
- creating only one identity this way can be guaranteed with the same trick TordadoCash uses to prevent double-spending: the [nullifier](https://docs.tornado.cash/how-does-tornado.cash-work) (don't ask me how that works)

I see two possible ways to solve 1), not sure which is easier:
  - a) Drop last SSN digit in favor of less sensitive data (that still gives high likelihood that name+bday+data is unique)
  - b) Include much more unique information, such that a preimage attack is infeasible (e.g. https://23andme.com ?)

