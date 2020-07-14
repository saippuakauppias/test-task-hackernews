#!/bin/sh

exit_not_zero() {
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
        exit_not_zero '1' 'Database wait failed'
    fi

    echo "Waiting for database to run (${SLEEP_ITER})..."
    sleep 0.5

    SLEEP_ITER=$((SLEEP_ITER+1))
done


# initialize database
hackernews init
exit_not_zero "$?" 'Database init failed'


# run cron daemon in background
/usr/sbin/crond -f -l 10 &
exit_not_zero "$?" 'Cron run failed'


# run server in foreground
hackernews serve --port 80 --host 0.0.0.0
exit_not_zero "$?" 'Server run failed'
