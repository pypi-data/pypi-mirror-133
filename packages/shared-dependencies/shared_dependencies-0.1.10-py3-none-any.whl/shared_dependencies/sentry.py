import os
import logging
from sentry_sdk import capture_exception, init
from sentry_sdk.integrations.pure_eval import PureEvalIntegration

logger = logging.getLogger("uvicorn")


def init_sentry(sentry_integrations: list, traces_sample_rate: float, sample_rate: float):
    """
    This method has to be called in the app init file (main.py).
    SENTRY_DSN, SENTRY_ENVIRONMENT and SENTRY_RELEASE must be provided in app variables.
    :param sentry_integrations:
    :param traces_sample_rate:
    :param sample_rate:
    :return: sentry init function
    """
    return init(
        integrations=sentry_integrations,
        traces_sample_rate=traces_sample_rate,
        sample_rate=sample_rate,
        traces_sampler=sampling_context,
    )


def sampling_context(context):
    try:
        if "/metrics" in context["asgi_scope"].get("path", ""):
            return 0
    except KeyError:
        logger.exception("context->asgi_scope failed")
        return 0
    else:
        logger.info(f'sentry-trace : {context["transaction_context"]["trace_id"]}')
        return float(os.getenv("TRACES_SAMPLE_RATE_SENTRY", 1.0))