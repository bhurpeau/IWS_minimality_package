import sys, numpy as np, time
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from nerode_R0_sequential import map_R0_sequential

amps_grid = np.repeat(np.linspace(0.5, 10.0, 20), 40)
angs_grid = np.tile(np.linspace(0, 352, 40), 20)
print("Grille : %d protocoles" % len(amps_grid))
t0=time.time()
theta1, theta2, alive_seq = map_R0_sequential(amps_grid, angs_grid)
print("  (%.1fs)" % (time.time()-t0))
np.save('phi7_amps.npy', amps_grid); np.save('phi7_angs.npy', angs_grid)
np.save('phi7_theta1.npy', theta1); np.save('phi7_theta2.npy', theta2); np.save('phi7_alive.npy', alive_seq)
print("sauvegarde OK, %d/%d valides" % (alive_seq.sum(), len(alive_seq)))
