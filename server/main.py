#!/usr/bin/env python3
import sys

print ("Enter your name:")                
sys.stdout.flush()
my_name = sys.stdin.readline().strip()
print ("Your name is %s" % my_name)
sys.stdout.flush()
quit()
