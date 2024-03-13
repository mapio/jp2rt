# A function converting MSP file to TSV file (while filtering out negative ion mode records and records with no SMILES)

import csv


def msp2tsv(src, dst, extra_keys=('INCHIKEY', 'NAME')):
  keys = (
    'RETENTIONTIME',
    *extra_keys,
    'SMILES',
  )
  keys_set = frozenset(keys)
  csv_writer = csv.writer(dst, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  record = {}
  for line in src:
    lines = line.strip()
    if not lines:
      if keys_set <= set(record.keys()) and 'IONMODE' in record and record['IONMODE'] == 'Positive':
        csv_writer.writerow(record[k] for k in keys)
      record = {}
    else:
      key, *value = lines.split(': ', 1)
      if value:
        record[key] = value[0]
