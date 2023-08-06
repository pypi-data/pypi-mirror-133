import argparse

import sm_icon_extractor as smie


def main():
    ap = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('-m', '--map', type=str, choices=smie.ICONMAPS.keys(), help='The IconMap to extract, will extract all IconMaps by default')
    ap.add_argument('-d', '--dest', default='.', type=str, help='The directory to extract to')
    args = ap.parse_args()
    
    smie.extract(smie.ICONMAPS[args.map] if args.map else None, args.dest, verbose=True)

if __name__ == '__main__':
  main()
