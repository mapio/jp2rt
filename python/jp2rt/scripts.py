from json import dumps
from pathlib import Path

import click

from jp2rt import (
  add_descriptors_via_tsv,
  descriptors,
  evaluate_model,
  list_ensemble_models,
  load_descriptors,
  load_model,
  load_retention_times,
  save_model,
  simple_ensemble_model_estimate,
)


@click.group()
def cli():
  pass


@click.command()
@click.argument('src', type=click.Path(exists=True, resolve_path=True))
@click.argument('dst', type=click.Path(writable=True, resolve_path=True))
def compute_descriptors(src, dst):
  """Computes molecular descriptions.

  Reads a tab separated values file with SMILES and producing another tab separated values file appending molecular descriptor values.

  \b
  SRC   The source tab separated values file (must contain SMILES on the last column).
  DST   The destination tab separated values file (will have the same columns of SRC, followed by molecular descriptor values).
  """  # noqa: E501
  add_descriptors_via_tsv(src, dst)


@click.command()
@click.option('--json', '-j', is_flag=True, help='Produces JSON output.')
def list_descriptors(json):
  "List the known molecular descriptors."
  if json:
    click.echo(dumps(descriptors(), indent=2))
  else:
    n = 1
    for name, desc in descriptors().items():
      click.echo(name)
      for d in desc:
        click.echo(f'\t{n}: {d}')
        n += 1


@click.command()
@click.argument('model', type=click.Path(exists=True, resolve_path=True))
@click.argument('src', type=click.Path(exists=True, resolve_path=True))
@click.argument('dst', type=click.Path(writable=True, resolve_path=True))
def predict_rt(model, src, dst):
  """Uses the model to predict the retention time.

  Given a tab separated values containing the molecular descriptors and a model, produces another tab separated values file prepending the predicted value.

  \b
  MODEL The model file.
  SRC   The source tab separated values file (the molecular descriptors must be on the last columns).
  DST   The destination tab separated values file (will have the predicted retention time, followed by the same columns of SRC).
  """  # noqa: E501
  model = load_model(model)
  X = load_descriptors(src)
  click.echo(f'Read {X.shape[0]} molecules with {X.shape[1]} descriptor values each...')
  y = model.predict(X)
  with open(src) as inf, open(dst, 'w') as ouf:
    for line, rt in zip(inf, y, strict=True):
      ouf.write(f'{rt}\t{line}')
  click.echo(f'Predicted retention times written to {dst}...')


@click.command()
@click.option('--evaluate', '-e', is_flag=True, help='Evaluates the model using cross-validation.')
@click.argument('name', type=click.STRING)
@click.argument('src', type=click.Path(exists=True, resolve_path=True))
@click.argument('dst', type=click.Path(writable=True, resolve_path=True))
def estimate_model(evaluate, name, src, dst):
  """Estimates a model using the given ensemble regressor.

  \b
  NAME  The ensemble regressor name.
  SRC   The source tab separated values file (the retention times must be on the first column, and molecular descriptors must be on the last columns).
  DST   The destination model file.
  """  # noqa: E501
  dst = Path(dst)
  X = load_descriptors(src)
  y = load_retention_times(src)
  click.echo(f'Read {X.shape[0]} molecules with {X.shape[1]} descriptor values each\nEstimating model...')
  model = simple_ensemble_model_estimate(name, X, y)
  size = save_model(model, dst)
  click.echo(f'Model saved to {dst.with_suffix(".jp2rt")} ({size} bytes)...')
  if evaluate:
    click.echo('Evaluating model...')
    v = evaluate_model(model, X, y)
    click.echo(v['table'])
    pdst = dst.with_suffix('.png')
    plot = v['plot']
    if plot:
      plot.savefig(pdst)
      click.echo(f'Evaluation plot saved to {pdst}')


@click.command()
def list_models():
  "List the known ensemble models."
  click.echo('\n'.join(list_ensemble_models()))


cli.add_command(compute_descriptors)
cli.add_command(estimate_model)
cli.add_command(list_descriptors)
cli.add_command(list_models)
cli.add_command(predict_rt)

if __name__ == '__main__':
  cli()
