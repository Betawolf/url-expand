import sys
import logging
import argparse
import transforms

if __name__ == '__main__':
  transforms = transforms.all_transforms()

  parser = argparse.ArgumentParser(description='Transform URLs in-place.')
  parser.add_argument('transformer', help='The transform to apply, one of:\n'+'\n'.join(transforms.keys()))
  parser.add_argument('infile',nargs='?',help='The input file containing text with shortened URLs. Default is STDIN.',default=sys.stdin,type=argparse.FileType('r'))
  parser.add_argument('outfile',nargs='?',help='Writeable output file. Default is STDOUT. ',default=sys.stdout,type=argparse.FileType('w'))
  parser.add_argument('--errors', '-e',nargs='?',help='Logfile for warnings. Default is STDERR.',default=sys.stderr,type=argparse.FileType('w'))
  args = parser.parse_args()

  if args.transformer not in transforms:
    logging.error('Do not recognise transform `{}`'.format(args.transformer))
    exit()

  transformer = transforms[args.transformer]()

  for line in args.infile:
    args.outfile.write(transformer.transform_in_place(line))
