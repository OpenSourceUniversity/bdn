import sys
import time
import ipfsapi


def main():
    api = ipfsapi.connect('https://ipfs.infura.io', port=5001)
    ipfs_hash = sys.argv[1]
    start = time.time()

    def get_from_ipfs():
        try:
            f = api.cat([ipfs_hash])
            print(len(f))
        except Exception:
            import traceback
            print(traceback.print_exc())
            print("Timeout. Retrying.")
            get_from_ipfs()
    get_from_ipfs()

    end = time.time()
    exec_time = end - start
    print('start', start)
    print('end', end)
    print('time', exec_time)


if __name__ == '__main__':
    main()
