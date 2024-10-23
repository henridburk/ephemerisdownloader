#!/bin/bash

FILE="gpssim.bin"
FREQUENCY=1575420000
SAMPLE_RATE=2600000
AMPLITUDE=1
TX_GAIN=0

# Function to handle termination
cleanup() {
    echo "Stopping transmission..."
    kill $PID  # Send kill signal to hackrf_transfer process
    wait $PID  # Wait for it to terminate
    exit 0     # Exit the script
}

# Trap signals
trap cleanup SIGINT SIGTERM

while true; do
    echo "Transmitting $FILE..."

    # Run the hackrf_transfer command in the background
    hackrf_transfer -t "$FILE" -f "$FREQUENCY" -s "$SAMPLE_RATE" -a "$AMPLITUDE" -x "$TX_GAIN" &
    PID=$!  # Capture the PID of hackrf_transfer

    # Wait for the hackrf_transfer to finish
    wait $PID

    # Check for the exit status of the previous command
    if [ $? -ne 0 ]; then
        echo "hackrf_transfer encountered an error. Exiting."
        break  # Exit the loop if there's an error
    fi

    echo "Looping back to transmit $FILE again..."
done

