#!/bin/bash
for filename in ./*.json; do
        mongoimport --uri ${MONGO_CONNECTION_STRING} \
                --db openAPITestDB --collection $(basename $filename .json) --file $filename --jsonArray --drop
done