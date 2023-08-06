import os

from pipeline_esbuild.conf import settings
from pipeline.compilers import SubProcessCompiler


class EsbuildCompiler(SubProcessCompiler):
    output_extension = 'js'

    def match_file(self, path):
        return path.endswith('.es6') or path.endswith('.js')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        """outfile should be a dist dir"""
        if not outdated and not force:
            return  # File doesn't need to be recompiled
        command = (
            settings.ESBUILD_BINARY,
            infile,
            settings.ESBUILD_ARGUMENTS,
            f"--outfile={outfile}"
        )
        return self.execute_command(command)
