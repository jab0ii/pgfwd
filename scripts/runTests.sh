#!/bin/bash
# Author: Noah Gold
pattern="tests*.py"
case $1 in
    unit)
        pattern="tests.py"
        ;;
    func)
        pattern="tests_func.py"
        ;;
    ui)
        pattern="ui_tests.py"
        ;;
    reset)
        rabbitmqctl stop_app
        rabbitmqctl reset
        rabbitmqctl start_app
        echo 'RabbitMQ queues cleared.'
        exit
        ;;
esac
foreman start worker &
foreman run python manage.py test --pattern=$pattern 
pkill -INT -P $!
kill -9 $!
