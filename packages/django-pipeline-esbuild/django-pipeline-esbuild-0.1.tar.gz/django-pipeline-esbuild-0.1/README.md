# Pipeline Esbuild

Django pipeline esbuild plugin adds support for esbuild bundles by using the
esbuil binary installed in the system.

## Instalation
```
pip install django-pipeline-esbuild
```

## Configuration

```python
PIPELINE['COMPILERS'] = (
  'pipeline_esbuild.esbuild.EsbuildCompiler',
)

# esbuild defaults
ESBUILD_BINARY = '/usr/bin/env esbuild'
ESBUILD_ARGUMENTS = '--bundle'
```
