#!/bin/bash

endpoint="http://127.0.0.1:5000"
numberOfRequests=1000 # Number of requests to send

start=$(date +%s%N)

for ((i = 1; i <= numberOfRequests; i++)); do
    response=$(curl -s -o /dev/null -w "%{http_code}" "$endpoint")
    echo "Request $i: $response"
done

end=$(date +%s%N)
totalTime=$((($end - $start) / 1000000)) # in milliseconds
averageResponseTime=$(($totalTime / $numberOfRequests))

echo "Total time taken: $totalTime ms"
echo "Average response time: $averageResponseTime ms"
