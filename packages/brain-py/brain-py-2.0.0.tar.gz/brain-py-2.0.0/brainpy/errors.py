# -*- coding: utf-8 -*-


class BrainPyError(Exception):
  """General BrainPy error."""
  pass


class ModelBuildError(BrainPyError):
  """The error occurred during the definition of models."""
  pass


class RunningError(BrainPyError):
  """The error occurred in the running function."""
  pass


class IntegratorError(BrainPyError):
  pass


class DiffEqError(BrainPyError):
  """The differential equation definition error."""
  pass


class CodeError(BrainPyError):
  """Code definition error.
  """
  pass


class AnalyzerError(BrainPyError):
  """Error occurred in differential equation analyzer and dynamics analysis.
  """


class PackageMissingError(BrainPyError):
  """The package missing error.
  """
  pass


class BackendNotInstalled(BrainPyError):
  def __init__(self, backend):
    super(BackendNotInstalled, self).__init__(
      '"{bk}" must be installed when the user wants to use {bk} backend. \n'
      'Please install {bk} through "pip install {bk}" '
      'or "conda install {bk}".'.format(bk=backend))


class UniqueNameError(BrainPyError):
  def __init__(self, *args):
    super(UniqueNameError, self).__init__(*args)


class UnsupportedError(BrainPyError):
  pass


class NoLongerSupportError(BrainPyError):
  pass


class ConnectorError(BrainPyError):
  pass


class MonitorError(BrainPyError):
  pass


class MathError(BrainPyError):
  """Errors occurred in ``brainpy.math`` module."""
  pass


class JaxTracerError(MathError):
  def __init__(self):
    super(JaxTracerError, self).__init__(
      'There is an unexpected tracer. \n\n'
      'In BrainPy, all the dynamically changed variables must be provided '
      'into the "dyn_vars" when calling the transformation functions, '
      'like "jit()", "vmap()", "grad()", "make_loop()", etc. \n\n'
      'We found there are changed variables which are not wrapped into '
      '"dyn_vars". Please check!'
    )
