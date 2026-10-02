"""
Rang/Jacobien de F2:(r,phi) -> (theta1,theta2) in T^2 (Benoit), avant de
construire le contre-exemple. Difference centree numerique sur une grille
de points (r,phi), batchee (4 evaluations voisines par point).
"""
import sys, numpy as np, time
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from nerode_R0_sequential import map_R0_sequential

def unwrap_near(angles_deg, ref_deg):
    """Deplie angles (deg) pour qu'ils soient proches de ref (evite le saut 360/0)."""
    d = (angles_deg - ref_deg + 180) % 360 - 180
    return ref_deg + d

def jacobian_F2(rs, phis, dr=0.05, dphi=1.0):
    M = len(rs)
    pts_r = np.concatenate([rs, rs+dr, rs-dr, rs, rs])
    pts_phi = np.concatenate([phis, phis, phis, phis+dphi, phis-dphi])
    th1_all, th2_all, alive_all = map_R0_sequential(pts_r, pts_phi)
    th1 = th1_all.reshape(5, M); th2 = th2_all.reshape(5, M); alive = alive_all.reshape(5, M)
    ok = alive.all(axis=0) & ~np.isnan(th1).any(axis=0) & ~np.isnan(th2).any(axis=0)

    th1_0 = th1[0]
    th1_pr, th1_mr, th1_pp, th1_mp = th1[1], th1[2], th1[3], th1[4]
    th2_0 = th2[0]
    th2_pr, th2_mr, th2_pp, th2_mp = th2[1], th2[2], th2[3], th2[4]

    def diffc(a_p, a_m, ref):
        return (unwrap_near(a_p, ref) - unwrap_near(a_m, ref))

    dth1_dr = diffc(th1_pr, th1_mr, th1_0) / (2*dr)
    dth1_dphi = diffc(th1_pp, th1_mp, th1_0) / (2*dphi)
    dth2_dr = diffc(th2_pr, th2_mr, th2_0) / (2*dr)
    dth2_dphi = diffc(th2_pp, th2_mp, th2_0) / (2*dphi)

    det = dth1_dr*dth2_dphi - dth1_dphi*dth2_dr
    # "rang < 2" approxime par un petit determinant RELATIF (normalise par la
    # norme de Frobenius du Jacobien, pour ne pas confondre "petit" avec
    # "jacobien globalement petit en magnitude")
    fro = np.sqrt(dth1_dr**2 + dth1_dphi**2 + dth2_dr**2 + dth2_dphi**2) + 1e-12
    det_rel = det / (fro**2)
    return dict(ok=ok, det=det, det_rel=det_rel, fro=fro,
                dth1_dr=dth1_dr, dth1_dphi=dth1_dphi, dth2_dr=dth2_dr, dth2_dphi=dth2_dphi)

if __name__ == '__main__':
    rs = np.repeat(np.linspace(0.6, 9.5, 20), 25)
    phis = np.tile(np.linspace(5, 355, 25), 20)
    print("Jacobien de F2 sur %d points (r,phi)" % len(rs))
    t0=time.time()
    res = jacobian_F2(rs, phis)
    print("  (%.1fs)" % (time.time()-t0))
    ok = res['ok']
    print("  %d/%d points valides (4 voisins + central tous atteignent k=2)" % (ok.sum(), len(ok)))
    det_rel = res['det_rel'][ok]
    print("  |det_rel| : min=%.4f  median=%.4f  max=%.4f" % (np.abs(det_rel).min(), np.median(np.abs(det_rel)), np.abs(det_rel).max()))
    frac_small = (np.abs(det_rel) < 0.05).mean()
    print("  fraction des points avec |det_rel|<0.05 (quasi-rang-1) : %.1f%%" % (100*frac_small))
    frac_tiny = (np.abs(det_rel) < 0.01).mean()
    print("  fraction avec |det_rel|<0.01 : %.1f%%" % (100*frac_tiny))

    np.save('R0_jac_rs.npy', rs); np.save('R0_jac_phis.npy', phis)
    np.save('R0_jac_det_rel.npy', res['det_rel']); np.save('R0_jac_ok.npy', ok)
    print("sauvegarde -> R0_jac_*.npy")
