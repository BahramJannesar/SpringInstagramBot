import argparse


def get_args():

  parser = argparse.ArgumentParser()
  parser.add_argument('-u', '--user', required=True, action='store', help='Username')
  parser.add_argument('-p', '--password', required=True, action='store', help='Password')
  parser.add_argument('-t', '--username_target', required=False, action='store', help='Target Username')
  parser.add_argument('-c', '--counts_of_follower', required=False, action='store', help='Counts of follower that you want to follow from target (more than 200)')

  my_args = parser.parse_args()
  return my_args

