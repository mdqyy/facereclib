#!/usr/bin/env python

import os

# The database to use
name = 'GBU'
protocol = 'Ugly'


database_dir = os.path.join(os.path.dirname(__file__), 'GBU')

img_input_dir = '/idiap/resource/database/MBGC-V1'
eye_file = os.path.join(database_dir, 'alleyes.csv')


training = os.path.join(database_dir, 'GBU_Training_x2.xml')
target   = os.path.join(database_dir, 'GBU_Ugly_Target.xml')
query    = os.path.join(database_dir, 'GBU_Ugly_Query.xml')
mask     = os.path.join(database_dir, 'GBU_Ugly_Mask.mtx')
