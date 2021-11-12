import unittest
import copy
import numpy
import scipy.linalg
import pyscf
from pyscf import semiempirical

class KnownValues(unittest.TestCase):
    def test_rmindo(self):
        mol = pyscf.M(atom=[(8,(0,0,0)),(1,(1.,0,0)),(1,(0,1.,0))])
        mf = semiempirical.RMINDO3(mol).run(conv_tol=1e-6)
        self.assertAlmostEqual(mf.e_heat_formation, -48.82621264564841, 6)

        mol = pyscf.M(atom=[(6,(0,0,0)),(1,(1.,0,0)),(1,(0,1.,0)),
                            (1,(0,0,1.)),(1,(0,0,-1.))])
        mf = semiempirical.RMINDO3(mol).run(conv_tol=1e-6)
        self.assertAlmostEqual(mf.e_heat_formation, 75.76019731515225, 6)

    def test_umindo(self):
        mol = pyscf.M(atom=[(8,(0,0,0)),(1,(1.,0,0))], spin=1)
        mf = semiempirical.UMINDO3(mol).run(conv_tol=1e-6)
        self.assertAlmostEqual(mf.e_heat_formation, 18.08247965492137)

if __name__ == "__main__":
    print("Full Tests for addons")
    unittest.main()
