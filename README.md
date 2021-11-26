# Proof of Legacy Identity

The current implementation has a major privacy issue, which can be split into two aspects: 
 1) Your ID basically reveals your name, birthday and last SSN digit, because a [Preimage Attack](https://en.wikipedia.org/wiki/Preimage_attack) is definitely feasible. That's why we're not using all last 4 digits, even though we could.
 2) your unique ID _is_ your unique digital identity that gets linked to your Ethereum account (e.g. allows anyone who knows your ID to find your transaction history). 

Number 2) should be solvable by literally copying the source code of [Tornado Cash](https://github.com/tornadocash). Logic: 
- user commits secretHash=hash(secret) while submitting ID
- contract aggregates all secretHash's into a single merkle tree
- a while later, user can create their actual unique digital identity by producing a zero-knowledge proof that they know a secret that hashes to a value that's contained in the merkle tree, without revealing which one.
- creating only one identity this way is guaranteed with the same trick tordado cash uses to prevent double-spending: the [nullifier](https://docs.tornado.cash/how-does-tornado.cash-work)

Two ways to solve 1):
  - a) Drop last SSN digit in favor of less sensitive data (that still gives high likelihood that name+bday+data is unique)
  - b) Include much more unique information, such that a preimage attack is infeasible (e.g. https://23andme.com ?)

