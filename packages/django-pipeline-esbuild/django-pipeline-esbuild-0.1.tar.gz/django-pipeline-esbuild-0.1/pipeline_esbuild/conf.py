from django.conf import settings as _settings

from pipeline.conf import PipelineSettings as _PipelineSettings, DEFAULTS as _DEFAULTS


DEFAULTS = {
    'ESBUILD_BINARY': '/usr/bin/env esbuild',
    'ESBUILD_ARGUMENTS': '--bundle',
}


class PipelineSettings(_PipelineSettings):
    def __init__(self, wrapped_settings):
        self.settings = DEFAULTS.copy()
        self.settings.update(_DEFAULTS)
        self.settings.update(wrapped_settings)


settings = PipelineSettings(_settings.PIPELINE)
