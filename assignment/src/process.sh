#!/bin/bash

# Parameters
WD="/home/hirama/Documents/assignment/"          # Working directory
YEAR="2023"                                      # Year (2023 or 2024)
MONTH="05"                                       # Month (e.g., 05) Note: Must be two digits!
DAY="10"                                         # Day (e.g., 15) Note: Must be two digits!
LAT=35.758252                                    # Latitude
LON=140.258344                                   # Longitude


# Get tile ID using Python script
output=$(python3 get_tileID.py "$LAT" "$LON")
V=$(echo "$output" | awk '{print $1}')
H=$(echo "$output" | awk '{print $2}')
imgX=$(echo "$output" | awk '{print $3}')
imgY=$(echo "$output" | awk '{print $4}')
V=$(printf "%02d" "$V")
H=$(printf "%02d" "$H")

# Check results
echo "V: $V, H: $H, imgX: $imgX, imgY: $imgY"

# Construct URL and file path
FILE_NAME="GC1SG1_${YEAR}${MONTH}${DAY}D01D_T${V}${H}_L2SG_RSRFQ_3002.h5"
URL="https://repo.gportal.jaxa.jp/standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/${YEAR}/${MONTH}/${DAY}/${FILE_NAME}"
SAVE_DIR="${WD}/data/${YEAR}/${MONTH}${DAY}/"
SAVE_PATH="${SAVE_DIR}${FILE_NAME}"

# Check if the file already exists
if [ -f "$SAVE_PATH" ]; then
    echo "File already exists: $SAVE_PATH. Skipping download."
else
    # Create the directory if it doesn't exist
    mkdir -p "$SAVE_DIR"

    # Download the file using wget
    wget "$URL" -P "$SAVE_DIR"

    # Check if the download was successful
    if [ $? -eq 0 ]; then
        echo "Download completed! File saved to ${SAVE_PATH}"
    else
        echo "Error: Failed to download the file from $URL"
    fi
fi

# Run Python script for processing
python3 assignment_sgli.py "$WD" "$YEAR" "$MONTH" "$DAY" "$V" "$H" "$imgX" "$imgY" "$SAVE_DIR"
