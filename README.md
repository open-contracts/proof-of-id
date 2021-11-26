# Proof of Legacy Identity

The current implementation has a major privacy issue, which can be split into two aspects: 
 1) ID reveals last ssn digits to anyone who guesses your name + bday (brute-force preimage attack only requires computing 10.000 hashes)
 2) your unique digital identity is linked to your identityHash (e.g. allows anyone who knows your legacy identity to pin down your new digital identity)

Number 2) should be solvable by literally copying the source code of [Tornado Cash](https://github.com/tornadocash). Logic: 
- user commits secretHash=hash(secret) while submitting identityHash
- contract aggregates all secretHash's into a single merkle tree
- a while later, user can create their new digital identity by producing a zero-knowledge proof that they know a secret that hashes to a value that's contained in the merkle tree, without revealing which one
- creating only one identity this way is guaranteed with the same trick tordado cash uses to prevent double-spending: the [nullifier](https://docs.tornado.cash/how-does-tornado.cash-work)

Two ways to solve 1):
  - a) Drop last 4 SSN digits in favor of less sensitive data (that still gives high likelihood that name+bday+data is unique)
  - b) Include much more unique information, such that a preimage attack is infeasible
 
 a) is probably easier than b), but still unsolved.
