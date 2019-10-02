import hashlib
import json
import requests

import sys


# TODO: Implement functionality to search for a proof 


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    def valid_proof(block_string, proof):
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:3] == "000"

    def proof_of_work(last_proof, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        print('block string -------------------------')
        print(block_string)
        proof = last_proof
        while valid_proof(block_string, proof) is False:
            proof += 1

        return proof

    coins_mined = 0

    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        response = requests.get(f'{node}/last-block')
        if response:
            print('Successful retrieval of last block.')
            last_block = response.json()['last_block']
            print(last_block)
            proof = last_block['proof']
            print('starting proof: ', proof)

            valid_proof = proof_of_work(proof, last_block)
            # TODO: When found, POST it to the server {"proof": new_proof}
            print('valid_proof', valid_proof)
            post_response = requests.post(f'{node}/mine', json={'proof': valid_proof})
            if post_response:
                print('Successful proof post')
                print(post_response.json())
            else:
                print(post_response.status_code)
                print(post_response.json())
                break

        else:
            print('Error while retrieving last block.')
            break
        
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.


