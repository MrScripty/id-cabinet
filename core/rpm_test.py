'''
Test module
'''

import rpmanager as rpm

rpm.Make(type='RPGRID', name='test_grid')
rpm.Make(type='ROW', name='test_grid', rows=[1, 3, 1])
rpm.Make(type='ROW', name='test_grid', rows=[0, -1, 0])

rpm.Make(type='RPGRID', name='spam')
rpm.Make(type='ROW', name='spam', rows=[4, 3, 1])

