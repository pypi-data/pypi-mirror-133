import os
from typing import List, Optional, Callable

from helios import HeliosBase, HeliosTags, version
from helios.instrumentation import default_instrumentation_list

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.util import types
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.trace.status import Status, StatusCode

SAMPLING_RATIO_RESOURCE_ATTRIBUTE_NAME = 'telemetry.sdk.sampling_ratio'
_OPENTELEMETRY_SDK_VERSION = version.__version__


class Helios(HeliosBase):
    def init_tracer_provider(self) -> TracerProvider:
        if self.resource_tags:
            resource_tags = self.resource_tags.copy()
        else:
            resource_tags = dict()
        resource_tags.update({
            ResourceAttributes.DEPLOYMENT_ENVIRONMENT:
                self.get_deployment_environment(),
            HeliosTags.ACCESS_TOKEN:
                self.api_token,
            ResourceAttributes.SERVICE_NAME:
                self.service_name,
            ResourceAttributes.TELEMETRY_SDK_VERSION:
                _OPENTELEMETRY_SDK_VERSION,
            ResourceAttributes.TELEMETRY_SDK_NAME:
                'helios-opentelemetry-sdk',
            SAMPLING_RATIO_RESOURCE_ATTRIBUTE_NAME:
                self.sampling_ratio
        })

        return TracerProvider(
            id_generator=self.id_generator,
            sampler=self.get_sampler(),
            resource=Resource.create(resource_tags),
        )

    def get_deployment_environment(self) -> str:

        if self.environment:
            return self.environment

        if self.resource_tags:
            deployment_environment = \
                self.resource_tags.get(
                    ResourceAttributes.DEPLOYMENT_ENVIRONMENT)

            if deployment_environment:
                return deployment_environment

        return os.environ.get('DEPLOYMENT_ENV', '')

    def get_sampler(self):
        if self.custom_sampler:
            return self.custom_sampler

        ratio = self.sampling_ratio or 1.0

        return TraceIdRatioBased(ratio)

    def create_custom_span(self, name: str, attributes: types.Attributes = None, wrapped_fn: Optional[Callable[[], any]] = None):
        tracer = self.tracer_provider.get_tracer('helios')
        with tracer.start_as_current_span(name, attributes=attributes) as custom_span:
            custom_span.set_attribute('hs-custom-span', 'true')
            if wrapped_fn is None:
                custom_span.end()
                return

            try:
                return wrapped_fn()
            except Exception as e:
                custom_span.set_status(Status(status_code=StatusCode.ERROR, description=str(e)))
                custom_span.record_exception(e)
                raise e
            finally:
                custom_span.end()

    def get_instrumentations(self) -> List[BaseInstrumentor]:
        return default_instrumentation_list
