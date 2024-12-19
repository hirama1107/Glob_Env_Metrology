#!/bin/bash

# Parameters
WD="/home/hirama/Documents/assignment/"          # Working directory
YEAR="2023"                                      # Year (e.g., 2023 or 2024)
START_MONTH="05"                                 # Start month (e.g., 05)
START_DAY="10"                                   # Start day (e.g., 10)
END_MONTH="05"                                   # End month (e.g., 05)
END_DAY="15"                                     # End day (e.g., 15)
LAT=35.758252                                    # Latitude
LON=140.258344                                   # Longitude


# Convert dates to a format that `date` can process
START_DATE="${YEAR}-${START_MONTH}-${START_DAY}"
END_DATE="${YEAR}-${END_MONTH}-${END_DAY}"

# Loop over each day in the range
current_date="$START_DATE"
while [[ "$current_date" < "$END_DATE" ]] || [[ "$current_date" == "$END_DATE" ]]; do
    # Extract the current month and day
    MONTH=$(date -d "$current_date" +%m)
    DAY=$(date -d "$current_date" +%d)

    # Get tile ID using Python script
    output=$(python3 get_tileID.py "$LAT" "$LON")
    V=$(echo "$output" | awk '{print $1}')
    H=$(echo "$output" | awk '{print $2}')
    imgX=$(echo "$output" | awk '{print $3}')
    imgY=$(echo "$output" | awk '{print $4}')
    V=$(printf "%02d" "$V")
    H=$(printf "%02d" "$H")

    # Check results
    echo "Processing for date: $current_date (V: $V, H: $H, imgX: $imgX, imgY: $imgY)"

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

    # Move to the next day
    current_date=$(date -d "$current_date + 1 day" +%Y-%m-%d)
done

