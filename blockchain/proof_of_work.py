import hashlib

def proof_of_work(last_proof):
    """
    Proof of work algorithm to find the next proof.
    It increments a proof value until a valid proof is found.
    """
    proof = 0
    while not valid_proof(last_proof, proof):
        proof += 1
    return proof

def valid_proof(last_proof, proof):
    """
    Check if the proof is valid.
    A valid proof is one where the hash of the last proof + current proof
    starts with four leading zeros (difficulty target).
    """
    guess = f"{last_proof}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"  # Example difficulty (4 leading zeros)
