import sys
import logging
import argparse
import urlmorph

if __name__ == '__main__':
  transformers = urlmorph.all_transforms()

  parser = argparse.ArgumentParser(description='Transform URLs in-place.')
  parser.add_argument('transformer', help='The transform to apply, one of {'+','.join(transformers.keys())+'}')
  parser.add_argument('infile',nargs='?',help='The input file containing text with shortened URLs. Default is STDIN.',default=sys.stdin,type=argparse.FileType('r'))
  parser.add_argument('outfile',nargs='?',help='Writeable output file. Default is STDOUT. ',default=sys.stdout,type=argparse.FileType('w'))
  parser.add_argument('--errors', '-e',nargs='?',help='Logfile for warnings. Default is STDERR.',default=sys.stderr)
  parser.add_argument('--args', '-a', nargs='*', help='Optional arguments to pass to the selected transform.')
  args = parser.parse_args()

  if args.errors != sys.stderr:
    logging.basicConfig(filename=args.errors,level=logging.INFO)

  if args.transformer not in transformers:
    logging.error('Do not recognise transform `{}`'.format(args.transformer))
    exit()

  if args.args:
    transformer = transformers[args.transformer](*args.args)
  else:
    transformer = transformers[args.transformer]()

  for line in args.infile:
    args.outfile.write(transformer.transform_in_place(line))
