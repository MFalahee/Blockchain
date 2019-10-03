import hashlib
import json
import requests
import time
import uuid
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

        return guess_hash[:6] == "000000"

    def proof_of_work(last_proof, block):
        block_string = json.dumps(block, sort_keys=True).encode()

        proof = last_proof
        while valid_proof(block_string, proof) is False:
            proof += 1

        return proof

    coins_mined = 0
    miner_id = uuid.uuid1().hex
    total_time_mining = 0

    # Run forever until interrupted
    while True:
        time_start = time.time()
        print('Total coins mined:', coins_mined)
        print('Total time spent mining:', round(total_time_mining, 2), 'seconds')
        # TODO: Get the last proof from the server and look for a new one
        response = requests.get(f'{node}/last_block')
        if response:
            last_block = response.json()['last_block']
            proof = last_block['proof']

            now = time.time()
            valid_proof_to_check = proof_of_work(proof, last_block)
            
            # TODO: When found, POST it to the server {"proof": new_proof}
            post_response = requests.post(f'{node}/mine', json={'proof': valid_proof_to_check, 'id': miner_id})
            if post_response:
                print('Successful proof post')
                print(post_response.json())
                coins_mined += 1
                time_finish = time.time()
                time_elapsed = (time_finish - time_start)
                total_time_mining += time_elapsed
                print('Time spent mining that coin: ', round(time_elapsed, 2), 'seconds')
            else:
                print('Failure to mine a coin')
                print(post_response.json())
        else:
            print('Error while retrieving last block.')
            break


