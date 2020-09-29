import argparse


def get_args():

  parser = argparse.ArgumentParser()
  parser.add_argument('-u', '--user', required=True, action='store', help='Username')
  parser.add_argument('-p', '--password', required=True, action='store', help='Password')
  parser.add_argument('-t', '--username_target', required=False, action='store', help='Target Username')
  parser.add_argument('-o', '--option', required=False, action='store', help='Option with likers or followers or commenters (LOL)')
  parser.add_argument('-cf', '--counts_of_follower', required=False, action='store', help='Counts of follower that you want to follow from target (more than 200)')
  parser.add_argument('-cl', '--counts_of_likers', required=False, action='store', help='Counts of likers that you want to follow from target')
  parser.add_argument('-cc', '--counts_of_commenters', required=False, action='store', help='Counts of commenters that you want to follow from target')
  my_args = parser.parse_args()
  return my_args

