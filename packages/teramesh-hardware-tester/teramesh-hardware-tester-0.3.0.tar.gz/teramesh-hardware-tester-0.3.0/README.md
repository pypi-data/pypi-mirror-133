
# Hardware Tester v.0.1-beta

## Prerequisites

If on RPi, `pip install teramesh-hardware-tester[rpi]`, otherwise `pip install teramesh-hardware-tester`.

If NOT on RPi, skip `-x test_relays`.

## List tests

    teramesh-hardware-test --no-tests-execute

## Run all tests on USB1

    teramesh-hardware-test -p /dev/ttyUSB1

## Run ONLY test_comms on USB1

    teramesh-hardware-test -p /dev/ttyUSB1 -i test_comms

## Run everything EXCEPT test_buzz on USB1

    teramesh-hardware-test -p /dev/ttyUSB1 -x test_buzz
