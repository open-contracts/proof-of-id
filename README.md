# Proof of Legacy Identity

The current implementation has a major privacy issue, which can be split into two aspects: 
 1) identityHash reveals last 4 ssn digits to anyone who guesses your name + bday (brute-force preimage attack only requires computing 10000 hashes)
 2) your unique digital identity is linked to your identityHash

Number 2) should be solvable by literally copying the source code of [Tornado Cash](https://github.com/tornadocash). Logic: 
- user commits secretHash=hash(secret) while submitting identityHash
- contract aggregates all secretHash's into a single merkle tree
- a while later, user can create their new digital identity by producing a zero-knowledge proof that they know a secret that hashes to a value that's contained in the merkle tree, without revealing which one
- creating only one identity this way is guaranteed with the same trick tordado cash uses to prevent double-spending: the [nullifier](https://docs.tornado.cash/how-does-tornado.cash-work)

Two ways to solve 1):
 a) Drop last 4 SSN digits in favor of something less sensitive (but unique enough to yield unique hashes - name+bday likely not enough)
 b) Included much more unique information, such that a preimage attach is infeasible
 
 a) is probably easier than b), but still unsolved.
