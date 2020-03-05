import logging
import random
import time
import os


# make default seed depend on process PID so that two processes spawned at the same time don't produce the same
# jitters
random.seed(time.time() * os.getpid())


def jitter_delay(delay):

    delay_with_jitter = (0.5 + 0.5 * random.random()) * delay
    time.sleep(delay_with_jitter)


def exponential_backoff(fun, max_retries, first_delay=1, jitter=True):
    """
    Calls fun() up to max_retries times until fun returns something other than None or throws an Exception.
    Waits twice as long after every try.

    :param fun:
        A function that performs a retryable operation.
        fun should:
         - return a value if the operation completed successfully
         - raise a RetryableException chained with the original Exception if the operation should be retried.
         - raise another Exception if we should give up immediately instead of retrying.
    :param max_retries:
        How many times the function call should be attempted before giving up.
    :param first_delay:
        A delay, in seconds, after the first retry.
    :param jitter:
        If true, will randomize the sleep time a bit to intentionally desync with other processes that potentially
         also wait for the same resource.
    :returns:
        The return value of fun if fun() eventually succeeded.
    :raises:
        The cause of the last RetryableException raised by fun if max_retries were reached
        The original Exception any other Exception was raised by fun

    """

    sleep = jitter_delay if jitter else time.sleep

    for retry in range(0, max_retries):
        try:
            return fun()
        except RetryableException as e:
            if retry == max_retries - 1:
                raise e.__cause__
        sleep(first_delay * (2 ** retry))


class RetryableException(Exception):
    pass
