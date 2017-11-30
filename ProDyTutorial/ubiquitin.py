from prody import *

ubi = parsePDB('2k39', subset='calpha')
ubi = ubi.select('resnum < 71')

ens = Ensemble('Ubiquitin')
ens.setCoords(ubi.getCoords())
ens.addCoordset(ubi.getCoordsets())

pca = PCA('Ubiquitin')
pca.buildCovariance(ens)
pca.calcModes(n_modes=None)

print(pca[0].getEigval())
u = pca[0].getEigvec()
v = pca[1].getEigvec()
print(u.dot(u))
print(u.dot(v))

showProjection(ens, pca[(0, 1)])

ubi.setACSIndex(78)
anm = ANM('Ubiquitin')
anm.buildHessian(ubi)
anm.calcModes(n_modes=None)

anm[0].getEigvec().dot(anm[1].getEigvec())

showProjection(ens, anm[(0, 1)])

print(anm[0].getEigvec().dot(pca[0].getEigvec()))

showOverlapTable(anm[:4], pca[:4])

showCrossProjection(ens, pca[1], anm[1])

printOverlapTable(anm[:4], pca[:4])
