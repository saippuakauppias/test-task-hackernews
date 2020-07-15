#!/bin/sh

exit_non_zero() {
    if [ "$1" -ne 0 ]
    then
        >&2 echo "$2"
        exit 1
    fi
}


# wait database start
SLEEP_ITER=0
SLEEP_MAX=60
while ! nc -z "${DB_HOST}" "${DB_PORT}"; do
    if [ ${SLEEP_ITER} -ge ${SLEEP_MAX} ]; then
        exit_non_zero '1' 'Database wait failed'
    fi

    echo "Waiting for database to run (${SLEEP_ITER})..."
    sleep 0.5

    SLEEP_ITER=$((SLEEP_ITER+1))
done


# initialize database
hackernews init
exit_non_zero "$?" 'Database init failed'


# run cron daemon in background
/usr/sbin/crond -f -l 10 &
exit_non_zero "$?" 'Cron run failed'


# run tests (TODO: need only in dev?)
pytest -v -l tests
exit_non_zero "$?" 'Tests failed'


# run server in foreground
hackernews serve --port 80 --host 0.0.0.0
exit_non_zero "$?" 'Server run failed'
