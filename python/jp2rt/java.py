import importlib.resources
from collections import OrderedDict

from scyjava import config, jimport, to_python

JP2RT_REF = ref = importlib.resources.files('jp2rt') / 'lib.jar'


class JavaLib:
  """
  A context manager allowing to import and use Java classes.
  """

  def __init__(self) -> None:
    self._cm = importlib.resources.as_file(JP2RT_REF)

  def __enter__(self):
    path = self._cm.__enter__()
    config.add_classpath(str(path))
    return lambda name: jimport(name) if '.' in name else jimport('it.unimi.di.jp2rt.' + name)

  def __exit__(self, exc_type, exc_value, traceback):
    return self._cm.__exit__(exc_type, exc_value, traceback)


def add_descriptors_via_tsv(src, dst):
  """Add molecular descriptors given the SMILES.

  The input file must be in tab separated format, must not have an header, and the
  SMILES must be the last fields of every row. In the output file will be copied
  all the fields of the input file, followed by the molecular descriptors values.

  Args:
    src (:obj:`str`): Path to the tab separated values file containing the SMILES.
    dst (:obj:`str`): Path to the tab separated values file to write the molecular descriptors.
  """
  with JavaLib() as jl:
    MDC = jl('MolecularDescriptorsCalculator')
    MDC.toFile(MDC.fromFile(src), dst)


def descriptors():
  """
  Returns the list of computed descriptors.

  The function returns a dictionary having the descriptor class names as keys
  and the name of the computed values.
  """
  with JavaLib() as jl:
    MDW = jl('MolecularDescriptorsWrapper')
    res = OrderedDict()
    for wd in MDW():
      res[str(wd.name())] = to_python(wd.descriptors())
    return res


def compute_descriptors(smiles):
  """
  Computes the descriptor values for the given SMILES.

  Args:
    smiles (:obj:`str`): The SMILES of the molecule of which the descriptors should be computed.

  Returns:
    :obj:`list` of :obj:`float`: the descriptor values.
  """
  with JavaLib() as jl:
    TSVRow = jl('TSVRow')
    MolecularDescriptorsWrapper = jl('MolecularDescriptorsWrapper')
    tsv_line = MolecularDescriptorsWrapper().calculate(TSVRow(smiles))
    return [float(_) for _ in tsv_line.descriptors()]


def compute_single_descriptor(name, smiles):
  """
  Computes the values of a given descriptor for the given SMILES.

  Args:
    name (:obj:`str`): The name of the class of the descriptor to compute.
    smiles (:obj:`str`): The SMILES of the molecule of which the descriptors should be computed.

  Returns:
    :obj:`list` of :obj:`float`: the descriptor values.
  """
  with JavaLib() as jl:
    SilentChemObjectBuilder = jl('org.openscience.cdk.silent.SilentChemObjectBuilder')
    SmilesParser = jl('org.openscience.cdk.smiles.SmilesParser')
    smilesParser = SmilesParser(SilentChemObjectBuilder())
    WrappedMolecularDescriptor = jl('WrappedMolecularDescriptor')
    Descriptor = jl(f'org.openscience.cdk.qsar.descriptors.molecular.{name}')
    wd = WrappedMolecularDescriptor(Descriptor())
    mol = smilesParser.parseSmiles(smiles)
    ds = wd.calculate(mol)
    return [float(_) for _ in ds.toArray()]
