import sglicod
import sys

def main():
    LAT = float(sys.argv[1])
    LON = float(sys.argv[2])

    V, H, imgX, imgY = sglicod.sgli_ll2tile_B0(4800, LON, LAT)
    print(f"{V} {H} {imgX} {imgY}")

if __name__ == "__main__":
    main()