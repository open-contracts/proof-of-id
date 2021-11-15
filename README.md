# Proof of Legacy Identity

Key issues: 
 1) last 4 ssn digits are revealed to anyone who knows your name + bday
 2) may want to prove uniqueness but 'start from scratch' in the beginning (without linking your new digital identity to your identityHash)

Number 2) should be solvable by literally copying the source code of [Tornado Cash](https://github.com/tornadocash). Logic: 
- user commits secretHash=hash(secret) while submitting identityHash
- contract aggregates all secretHash's into a single merkle tree
- a while later, user can create their new digital identity by producing a zero-knowledge proof that they know a secret that hashes to a value that's contained in the merkle tree, without revealing which one
- creating only one identity this way is guaranteed with the same trick tordado cash uses to prevent double-spending: the [nullifier](https://docs.tornado.cash/how-does-tornado.cash-work)
