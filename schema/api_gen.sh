#!/bin/sh
PARENT=$(dirname $PWD)
echo $PARENT
docker run --rm -v ${PARENT}:/local swaggerapi/swagger-codegen-cli generate -i /local/schema/swagger.yml -l typescript -o /local/front/src/api/gen
