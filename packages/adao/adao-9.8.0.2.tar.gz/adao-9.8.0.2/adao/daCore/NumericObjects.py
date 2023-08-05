# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2021 EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

__doc__ = """
    Définit les objets numériques génériques.
"""
__author__ = "Jean-Philippe ARGAUD"

import os, time, copy, types, sys, logging
import math, numpy, scipy, scipy.optimize, scipy.version
from daCore.BasicObjects import Operator, Covariance, PartialAlgorithm
from daCore.PlatformInfo import PlatformInfo
mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()
# logging.getLogger().setLevel(logging.DEBUG)

# ==============================================================================
def ExecuteFunction( triplet ):
    assert len(triplet) == 3, "Incorrect number of arguments"
    X, xArgs, funcrepr = triplet
    __X = numpy.ravel( X ).reshape((-1,1))
    __sys_path_tmp = sys.path ; sys.path.insert(0,funcrepr["__userFunction__path"])
    __module = __import__(funcrepr["__userFunction__modl"], globals(), locals(), [])
    __fonction = getattr(__module,funcrepr["__userFunction__name"])
    sys.path = __sys_path_tmp ; del __sys_path_tmp
    if isinstance(xArgs, dict):
        __HX  = __fonction( __X, **xArgs )
    else:
        __HX  = __fonction( __X )
    return numpy.ravel( __HX )

# ==============================================================================
class FDApproximation(object):
    """
    Cette classe sert d'interface pour définir les opérateurs approximés. A la
    création d'un objet, en fournissant une fonction "Function", on obtient un
    objet qui dispose de 3 méthodes "DirectOperator", "TangentOperator" et
    "AdjointOperator". On contrôle l'approximation DF avec l'incrément
    multiplicatif "increment" valant par défaut 1%, ou avec l'incrément fixe
    "dX" qui sera multiplié par "increment" (donc en %), et on effectue de DF
    centrées si le booléen "centeredDF" est vrai.
    """
    def __init__(self,
            name                  = "FDApproximation",
            Function              = None,
            centeredDF            = False,
            increment             = 0.01,
            dX                    = None,
            extraArguments        = None,
            reducingMemoryUse     = False,
            avoidingRedundancy    = True,
            toleranceInRedundancy = 1.e-18,
            lenghtOfRedundancy    = -1,
            mpEnabled             = False,
            mpWorkers             = None,
            mfEnabled             = False,
            ):
        self.__name = str(name)
        self.__extraArgs = extraArguments
        #
        if mpEnabled:
            try:
                import multiprocessing
                self.__mpEnabled = True
            except ImportError:
                self.__mpEnabled = False
        else:
            self.__mpEnabled = False
        self.__mpWorkers = mpWorkers
        if self.__mpWorkers is not None and self.__mpWorkers < 1:
            self.__mpWorkers = None
        logging.debug("FDA Calculs en multiprocessing : %s (nombre de processus : %s)"%(self.__mpEnabled,self.__mpWorkers))
        #
        self.__mfEnabled = bool(mfEnabled)
        logging.debug("FDA Calculs en multifonctions : %s"%(self.__mfEnabled,))
        #
        self.__rmEnabled = bool(reducingMemoryUse)
        logging.debug("FDA Calculs avec réduction mémoire : %s"%(self.__rmEnabled,))
        #
        if avoidingRedundancy:
            self.__avoidRC = True
            self.__tolerBP = float(toleranceInRedundancy)
            self.__lenghtRJ = int(lenghtOfRedundancy)
            self.__listJPCP = [] # Jacobian Previous Calculated Points
            self.__listJPCI = [] # Jacobian Previous Calculated Increment
            self.__listJPCR = [] # Jacobian Previous Calculated Results
            self.__listJPPN = [] # Jacobian Previous Calculated Point Norms
            self.__listJPIN = [] # Jacobian Previous Calculated Increment Norms
        else:
            self.__avoidRC = False
        logging.debug("FDA Calculs avec réduction des doublons : %s"%self.__avoidRC)
        if self.__avoidRC:
            logging.debug("FDA Tolérance de détermination des doublons : %.2e"%self.__tolerBP)
        #
        if self.__mpEnabled:
            if isinstance(Function,types.FunctionType):
                logging.debug("FDA Calculs en multiprocessing : FunctionType")
                self.__userFunction__name = Function.__name__
                try:
                    mod = os.path.join(Function.__globals__['filepath'],Function.__globals__['filename'])
                except:
                    mod = os.path.abspath(Function.__globals__['__file__'])
                if not os.path.isfile(mod):
                    raise ImportError("No user defined function or method found with the name %s"%(mod,))
                self.__userFunction__modl = os.path.basename(mod).replace('.pyc','').replace('.pyo','').replace('.py','')
                self.__userFunction__path = os.path.dirname(mod)
                del mod
                self.__userOperator = Operator( name = self.__name, fromMethod = Function, avoidingRedundancy = self.__avoidRC, inputAsMultiFunction = self.__mfEnabled, extraArguments = self.__extraArgs )
                self.__userFunction = self.__userOperator.appliedTo # Pour le calcul Direct
            elif isinstance(Function,types.MethodType):
                logging.debug("FDA Calculs en multiprocessing : MethodType")
                self.__userFunction__name = Function.__name__
                try:
                    mod = os.path.join(Function.__globals__['filepath'],Function.__globals__['filename'])
                except:
                    mod = os.path.abspath(Function.__func__.__globals__['__file__'])
                if not os.path.isfile(mod):
                    raise ImportError("No user defined function or method found with the name %s"%(mod,))
                self.__userFunction__modl = os.path.basename(mod).replace('.pyc','').replace('.pyo','').replace('.py','')
                self.__userFunction__path = os.path.dirname(mod)
                del mod
                self.__userOperator = Operator( name = self.__name, fromMethod = Function, avoidingRedundancy = self.__avoidRC, inputAsMultiFunction = self.__mfEnabled, extraArguments = self.__extraArgs )
                self.__userFunction = self.__userOperator.appliedTo # Pour le calcul Direct
            else:
                raise TypeError("User defined function or method has to be provided for finite differences approximation.")
        else:
            self.__userOperator = Operator( name = self.__name, fromMethod = Function, avoidingRedundancy = self.__avoidRC, inputAsMultiFunction = self.__mfEnabled, extraArguments = self.__extraArgs )
            self.__userFunction = self.__userOperator.appliedTo
        #
        self.__centeredDF = bool(centeredDF)
        if abs(float(increment)) > 1.e-15:
            self.__increment  = float(increment)
        else:
            self.__increment  = 0.01
        if dX is None:
            self.__dX     = None
        else:
            self.__dX     = numpy.ravel( dX )

    # ---------------------------------------------------------
    def __doublon__(self, e, l, n, v=None):
        __ac, __iac = False, -1
        for i in range(len(l)-1,-1,-1):
            if numpy.linalg.norm(e - l[i]) < self.__tolerBP * n[i]:
                __ac, __iac = True, i
                if v is not None: logging.debug("FDA Cas%s déja calculé, récupération du doublon %i"%(v,__iac))
                break
        return __ac, __iac

    # ---------------------------------------------------------
    def __listdotwith__(self, __LMatrix, __dotWith = None, __dotTWith = None):
        "Produit incrémental d'une matrice liste de colonnes avec un vecteur"
        if not isinstance(__LMatrix, (list,tuple)):
            raise TypeError("Columnwise list matrix has not the proper type: %s"%type(__LMatrix))
        if __dotWith is not None:
            __Idwx = numpy.ravel( __dotWith )
            assert len(__LMatrix) == __Idwx.size, "Incorrect size of elements"
            __Produit = numpy.zeros(__LMatrix[0].size)
            for i, col in enumerate(__LMatrix):
                __Produit += float(__Idwx[i]) * col
            return __Produit
        elif __dotTWith is not None:
            _Idwy = numpy.ravel( __dotTWith ).T
            assert __LMatrix[0].size == _Idwy.size, "Incorrect size of elements"
            __Produit = numpy.zeros(len(__LMatrix))
            for i, col in enumerate(__LMatrix):
                __Produit[i] = float( _Idwy @ col)
            return __Produit
        else:
            __Produit = None
        return __Produit

    # ---------------------------------------------------------
    def DirectOperator(self, X, **extraArgs ):
        """
        Calcul du direct à l'aide de la fonction fournie.

        NB : les extraArgs sont là pour assurer la compatibilité d'appel, mais
        ne doivent pas être données ici à la fonction utilisateur.
        """
        logging.debug("FDA Calcul DirectOperator (explicite)")
        if self.__mfEnabled:
            _HX = self.__userFunction( X, argsAsSerie = True )
        else:
            _HX = numpy.ravel(self.__userFunction( numpy.ravel(X) ))
        #
        return _HX

    # ---------------------------------------------------------
    def TangentMatrix(self, X, dotWith = None, dotTWith = None ):
        """
        Calcul de l'opérateur tangent comme la Jacobienne par différences finies,
        c'est-à-dire le gradient de H en X. On utilise des différences finies
        directionnelles autour du point X. X est un numpy.ndarray.

        Différences finies centrées (approximation d'ordre 2):
        1/ Pour chaque composante i de X, on ajoute et on enlève la perturbation
           dX[i] à la  composante X[i], pour composer X_plus_dXi et X_moins_dXi, et
           on calcule les réponses HX_plus_dXi = H( X_plus_dXi ) et HX_moins_dXi =
           H( X_moins_dXi )
        2/ On effectue les différences (HX_plus_dXi-HX_moins_dXi) et on divise par
           le pas 2*dXi
        3/ Chaque résultat, par composante, devient une colonne de la Jacobienne

        Différences finies non centrées (approximation d'ordre 1):
        1/ Pour chaque composante i de X, on ajoute la perturbation dX[i] à la
           composante X[i] pour composer X_plus_dXi, et on calcule la réponse
           HX_plus_dXi = H( X_plus_dXi )
        2/ On calcule la valeur centrale HX = H(X)
        3/ On effectue les différences (HX_plus_dXi-HX) et on divise par
           le pas dXi
        4/ Chaque résultat, par composante, devient une colonne de la Jacobienne

        """
        logging.debug("FDA Début du calcul de la Jacobienne")
        logging.debug("FDA   Incrément de............: %s*X"%float(self.__increment))
        logging.debug("FDA   Approximation centrée...: %s"%(self.__centeredDF))
        #
        if X is None or len(X)==0:
            raise ValueError("Nominal point X for approximate derivatives can not be None or void (given X: %s)."%(str(X),))
        #
        _X = numpy.ravel( X )
        #
        if self.__dX is None:
            _dX  = self.__increment * _X
        else:
            _dX = numpy.ravel( self.__dX )
        assert len(_X) == len(_dX), "Inconsistent dX increment length with respect to the X one"
        assert _X.size == _dX.size, "Inconsistent dX increment size with respect to the X one"
        #
        if (_dX == 0.).any():
            moyenne = _dX.mean()
            if moyenne == 0.:
                _dX = numpy.where( _dX == 0., float(self.__increment), _dX )
            else:
                _dX = numpy.where( _dX == 0., moyenne, _dX )
        #
        __alreadyCalculated  = False
        if self.__avoidRC:
            __bidon, __alreadyCalculatedP = self.__doublon__(_X,  self.__listJPCP, self.__listJPPN, None)
            __bidon, __alreadyCalculatedI = self.__doublon__(_dX, self.__listJPCI, self.__listJPIN, None)
            if __alreadyCalculatedP == __alreadyCalculatedI > -1:
                __alreadyCalculated, __i = True, __alreadyCalculatedP
                logging.debug("FDA Cas J déjà calculé, récupération du doublon %i"%__i)
        #
        if __alreadyCalculated:
            logging.debug("FDA   Calcul Jacobienne (par récupération du doublon %i)"%__i)
            _Jacobienne = self.__listJPCR[__i]
            logging.debug("FDA Fin du calcul de la Jacobienne")
            if dotWith is not None:
                return numpy.dot(_Jacobienne,   numpy.ravel( dotWith ))
            elif dotTWith is not None:
                return numpy.dot(_Jacobienne.T, numpy.ravel( dotTWith ))
        else:
            logging.debug("FDA   Calcul Jacobienne (explicite)")
            if self.__centeredDF:
                #
                if self.__mpEnabled and not self.__mfEnabled:
                    funcrepr = {
                        "__userFunction__path" : self.__userFunction__path,
                        "__userFunction__modl" : self.__userFunction__modl,
                        "__userFunction__name" : self.__userFunction__name,
                    }
                    _jobs = []
                    for i in range( len(_dX) ):
                        _dXi            = _dX[i]
                        _X_plus_dXi     = numpy.array( _X, dtype=float )
                        _X_plus_dXi[i]  = _X[i] + _dXi
                        _X_moins_dXi    = numpy.array( _X, dtype=float )
                        _X_moins_dXi[i] = _X[i] - _dXi
                        #
                        _jobs.append( (_X_plus_dXi,  self.__extraArgs, funcrepr) )
                        _jobs.append( (_X_moins_dXi, self.__extraArgs, funcrepr) )
                    #
                    import multiprocessing
                    self.__pool = multiprocessing.Pool(self.__mpWorkers)
                    _HX_plusmoins_dX = self.__pool.map( ExecuteFunction, _jobs )
                    self.__pool.close()
                    self.__pool.join()
                    #
                    _Jacobienne  = []
                    for i in range( len(_dX) ):
                        _Jacobienne.append( numpy.ravel( _HX_plusmoins_dX[2*i] - _HX_plusmoins_dX[2*i+1] ) / (2.*_dX[i]) )
                    #
                elif self.__mfEnabled:
                    _xserie = []
                    for i in range( len(_dX) ):
                        _dXi            = _dX[i]
                        _X_plus_dXi     = numpy.array( _X, dtype=float )
                        _X_plus_dXi[i]  = _X[i] + _dXi
                        _X_moins_dXi    = numpy.array( _X, dtype=float )
                        _X_moins_dXi[i] = _X[i] - _dXi
                        #
                        _xserie.append( _X_plus_dXi )
                        _xserie.append( _X_moins_dXi )
                    #
                    _HX_plusmoins_dX = self.DirectOperator( _xserie )
                     #
                    _Jacobienne  = []
                    for i in range( len(_dX) ):
                        _Jacobienne.append( numpy.ravel( _HX_plusmoins_dX[2*i] - _HX_plusmoins_dX[2*i+1] ) / (2.*_dX[i]) )
                    #
                else:
                    _Jacobienne  = []
                    for i in range( _dX.size ):
                        _dXi            = _dX[i]
                        _X_plus_dXi     = numpy.array( _X, dtype=float )
                        _X_plus_dXi[i]  = _X[i] + _dXi
                        _X_moins_dXi    = numpy.array( _X, dtype=float )
                        _X_moins_dXi[i] = _X[i] - _dXi
                        #
                        _HX_plus_dXi    = self.DirectOperator( _X_plus_dXi )
                        _HX_moins_dXi   = self.DirectOperator( _X_moins_dXi )
                        #
                        _Jacobienne.append( numpy.ravel( _HX_plus_dXi - _HX_moins_dXi ) / (2.*_dXi) )
                #
            else:
                #
                if self.__mpEnabled and not self.__mfEnabled:
                    funcrepr = {
                        "__userFunction__path" : self.__userFunction__path,
                        "__userFunction__modl" : self.__userFunction__modl,
                        "__userFunction__name" : self.__userFunction__name,
                    }
                    _jobs = []
                    _jobs.append( (_X, self.__extraArgs, funcrepr) )
                    for i in range( len(_dX) ):
                        _X_plus_dXi    = numpy.array( _X, dtype=float )
                        _X_plus_dXi[i] = _X[i] + _dX[i]
                        #
                        _jobs.append( (_X_plus_dXi, self.__extraArgs, funcrepr) )
                    #
                    import multiprocessing
                    self.__pool = multiprocessing.Pool(self.__mpWorkers)
                    _HX_plus_dX = self.__pool.map( ExecuteFunction, _jobs )
                    self.__pool.close()
                    self.__pool.join()
                    #
                    _HX = _HX_plus_dX.pop(0)
                    #
                    _Jacobienne = []
                    for i in range( len(_dX) ):
                        _Jacobienne.append( numpy.ravel(( _HX_plus_dX[i] - _HX ) / _dX[i]) )
                    #
                elif self.__mfEnabled:
                    _xserie = []
                    _xserie.append( _X )
                    for i in range( len(_dX) ):
                        _X_plus_dXi    = numpy.array( _X, dtype=float )
                        _X_plus_dXi[i] = _X[i] + _dX[i]
                        #
                        _xserie.append( _X_plus_dXi )
                    #
                    _HX_plus_dX = self.DirectOperator( _xserie )
                    #
                    _HX = _HX_plus_dX.pop(0)
                    #
                    _Jacobienne = []
                    for i in range( len(_dX) ):
                        _Jacobienne.append( numpy.ravel(( _HX_plus_dX[i] - _HX ) / _dX[i]) )
                   #
                else:
                    _Jacobienne  = []
                    _HX = self.DirectOperator( _X )
                    for i in range( _dX.size ):
                        _dXi            = _dX[i]
                        _X_plus_dXi     = numpy.array( _X, dtype=float )
                        _X_plus_dXi[i]  = _X[i] + _dXi
                        #
                        _HX_plus_dXi = self.DirectOperator( _X_plus_dXi )
                        #
                        _Jacobienne.append( numpy.ravel(( _HX_plus_dXi - _HX ) / _dXi) )
            #
            if (dotWith is not None) or (dotTWith is not None):
                __Produit = self.__listdotwith__(_Jacobienne, dotWith, dotTWith)
            else:
                __Produit = None
            if __Produit is None or self.__avoidRC:
                _Jacobienne = numpy.transpose( numpy.vstack( _Jacobienne ) )
                if self.__avoidRC:
                    if self.__lenghtRJ < 0: self.__lenghtRJ = 2 * _X.size
                    while len(self.__listJPCP) > self.__lenghtRJ:
                        self.__listJPCP.pop(0)
                        self.__listJPCI.pop(0)
                        self.__listJPCR.pop(0)
                        self.__listJPPN.pop(0)
                        self.__listJPIN.pop(0)
                    self.__listJPCP.append( copy.copy(_X) )
                    self.__listJPCI.append( copy.copy(_dX) )
                    self.__listJPCR.append( copy.copy(_Jacobienne) )
                    self.__listJPPN.append( numpy.linalg.norm(_X) )
                    self.__listJPIN.append( numpy.linalg.norm(_Jacobienne) )
            logging.debug("FDA Fin du calcul de la Jacobienne")
            if __Produit is not None:
                return __Produit
        #
        return _Jacobienne

    # ---------------------------------------------------------
    def TangentOperator(self, paire, **extraArgs ):
        """
        Calcul du tangent à l'aide de la Jacobienne.

        NB : les extraArgs sont là pour assurer la compatibilité d'appel, mais
        ne doivent pas être données ici à la fonction utilisateur.
        """
        if self.__mfEnabled:
            assert len(paire) == 1, "Incorrect length of arguments"
            _paire = paire[0]
            assert len(_paire) == 2, "Incorrect number of arguments"
        else:
            assert len(paire) == 2, "Incorrect number of arguments"
            _paire = paire
        X, dX = _paire
        if dX is None or len(dX) == 0:
            #
            # Calcul de la forme matricielle si le second argument est None
            # -------------------------------------------------------------
            _Jacobienne = self.TangentMatrix( X )
            if self.__mfEnabled: return [_Jacobienne,]
            else:                return _Jacobienne
        else:
            #
            # Calcul de la valeur linéarisée de H en X appliqué à dX
            # ------------------------------------------------------
            _HtX = self.TangentMatrix( X, dotWith = dX )
            if self.__mfEnabled: return [_HtX,]
            else:                return _HtX

    # ---------------------------------------------------------
    def AdjointOperator(self, paire, **extraArgs ):
        """
        Calcul de l'adjoint à l'aide de la Jacobienne.

        NB : les extraArgs sont là pour assurer la compatibilité d'appel, mais
        ne doivent pas être données ici à la fonction utilisateur.
        """
        if self.__mfEnabled:
            assert len(paire) == 1, "Incorrect length of arguments"
            _paire = paire[0]
            assert len(_paire) == 2, "Incorrect number of arguments"
        else:
            assert len(paire) == 2, "Incorrect number of arguments"
            _paire = paire
        X, Y = _paire
        if Y is None or len(Y) == 0:
            #
            # Calcul de la forme matricielle si le second argument est None
            # -------------------------------------------------------------
            _JacobienneT = self.TangentMatrix( X ).T
            if self.__mfEnabled: return [_JacobienneT,]
            else:                return _JacobienneT
        else:
            #
            # Calcul de la valeur de l'adjoint en X appliqué à Y
            # --------------------------------------------------
            _HaY = self.TangentMatrix( X, dotTWith = Y )
            if self.__mfEnabled: return [_HaY,]
            else:                return _HaY

# ==============================================================================
def EnsembleOfCenteredPerturbations( _bgcenter, _bgcovariance, _nbmembers ):
    "Génération d'un ensemble de taille _nbmembers-1 d'états aléatoires centrés"
    #
    _bgcenter = numpy.ravel(_bgcenter)[:,None]
    if _nbmembers < 1:
        raise ValueError("Number of members has to be strictly more than 1 (given number: %s)."%(str(_nbmembers),))
    #
    if _bgcovariance is None:
        _Perturbations = numpy.tile( _bgcenter, _nbmembers)
    else:
        _Z = numpy.random.multivariate_normal(numpy.zeros(_bgcenter.size), _bgcovariance, size=_nbmembers).T
        _Perturbations = numpy.tile( _bgcenter, _nbmembers) + _Z
    #
    return _Perturbations

# ==============================================================================
def EnsembleOfBackgroundPerturbations( _bgcenter, _bgcovariance, _nbmembers, _withSVD = True):
    "Génération d'un ensemble de taille _nbmembers-1 d'états aléatoires centrés"
    def __CenteredRandomAnomalies(Zr, N):
        """
        Génère une matrice de N anomalies aléatoires centrées sur Zr selon les
        notes manuscrites de MB et conforme au code de PS avec eps = -1
        """
        eps = -1
        Q = numpy.identity(N-1)-numpy.ones((N-1,N-1))/numpy.sqrt(N)/(numpy.sqrt(N)-eps)
        Q = numpy.concatenate((Q, [eps*numpy.ones(N-1)/numpy.sqrt(N)]), axis=0)
        R, _ = numpy.linalg.qr(numpy.random.normal(size = (N-1,N-1)))
        Q = numpy.dot(Q,R)
        Zr = numpy.dot(Q,Zr)
        return Zr.T
    #
    _bgcenter = numpy.ravel(_bgcenter).reshape((-1,1))
    if _nbmembers < 1:
        raise ValueError("Number of members has to be strictly more than 1 (given number: %s)."%(str(_nbmembers),))
    if _bgcovariance is None:
        _Perturbations = numpy.tile( _bgcenter, _nbmembers)
    else:
        if _withSVD:
            _U, _s, _V = numpy.linalg.svd(_bgcovariance, full_matrices=False)
            _nbctl = _bgcenter.size
            if _nbmembers > _nbctl:
                _Z = numpy.concatenate((numpy.dot(
                    numpy.diag(numpy.sqrt(_s[:_nbctl])), _V[:_nbctl]),
                    numpy.random.multivariate_normal(numpy.zeros(_nbctl),_bgcovariance,_nbmembers-1-_nbctl)), axis = 0)
            else:
                _Z = numpy.dot(numpy.diag(numpy.sqrt(_s[:_nbmembers-1])), _V[:_nbmembers-1])
            _Zca = __CenteredRandomAnomalies(_Z, _nbmembers)
            _Perturbations = _bgcenter + _Zca
        else:
            if max(abs(_bgcovariance.flatten())) > 0:
                _nbctl = _bgcenter.size
                _Z = numpy.random.multivariate_normal(numpy.zeros(_nbctl),_bgcovariance,_nbmembers-1)
                _Zca = __CenteredRandomAnomalies(_Z, _nbmembers)
                _Perturbations = _bgcenter + _Zca
            else:
                _Perturbations = numpy.tile( _bgcenter, _nbmembers)
    #
    return _Perturbations

# ==============================================================================
def EnsembleMean( __Ensemble ):
    "Renvoie la moyenne empirique d'un ensemble"
    return numpy.asarray(__Ensemble).mean(axis=1, dtype=mfp).astype('float').reshape((-1,1))

# ==============================================================================
def EnsembleOfAnomalies( __Ensemble, __OptMean = None, __Normalisation = 1.):
    "Renvoie les anomalies centrées à partir d'un ensemble"
    if __OptMean is None:
        __Em = EnsembleMean( __Ensemble )
    else:
        __Em = numpy.ravel( __OptMean ).reshape((-1,1))
    #
    return __Normalisation * (numpy.asarray( __Ensemble ) - __Em)

# ==============================================================================
def EnsembleErrorCovariance( __Ensemble, __quick = False ):
    "Renvoie l'estimation empirique de la covariance d'ensemble"
    if __quick:
        # Covariance rapide mais rarement définie positive
        __Covariance = numpy.cov( __Ensemble )
    else:
        # Résultat souvent identique à numpy.cov, mais plus robuste
        __n, __m = numpy.asarray( __Ensemble ).shape
        __Anomalies = EnsembleOfAnomalies( __Ensemble )
        # Estimation empirique
        __Covariance = ( __Anomalies @ __Anomalies.T ) / (__m-1)
        # Assure la symétrie
        __Covariance = ( __Covariance + __Covariance.T ) * 0.5
        # Assure la positivité
        __epsilon    = mpr*numpy.trace( __Covariance )
        __Covariance = __Covariance + __epsilon * numpy.identity(__n)
    #
    return __Covariance

# ==============================================================================
def EnsemblePerturbationWithGivenCovariance( __Ensemble, __Covariance, __Seed=None ):
    "Ajout d'une perturbation à chaque membre d'un ensemble selon une covariance prescrite"
    if hasattr(__Covariance,"assparsematrix"):
        if (abs(__Ensemble).mean() > mpr) and (abs(__Covariance.assparsematrix())/abs(__Ensemble).mean() < mpr).all():
            # Traitement d'une covariance nulle ou presque
            return __Ensemble
        if (abs(__Ensemble).mean() <= mpr) and (abs(__Covariance.assparsematrix()) < mpr).all():
            # Traitement d'une covariance nulle ou presque
            return __Ensemble
    else:
        if (abs(__Ensemble).mean() > mpr) and (abs(__Covariance)/abs(__Ensemble).mean() < mpr).all():
            # Traitement d'une covariance nulle ou presque
            return __Ensemble
        if (abs(__Ensemble).mean() <= mpr) and (abs(__Covariance) < mpr).all():
            # Traitement d'une covariance nulle ou presque
            return __Ensemble
    #
    __n, __m = __Ensemble.shape
    if __Seed is not None: numpy.random.seed(__Seed)
    #
    if hasattr(__Covariance,"isscalar") and __Covariance.isscalar():
        # Traitement d'une covariance multiple de l'identité
        __zero = 0.
        __std  = numpy.sqrt(__Covariance.assparsematrix())
        __Ensemble += numpy.random.normal(__zero, __std, size=(__m,__n)).T
    #
    elif hasattr(__Covariance,"isvector") and __Covariance.isvector():
        # Traitement d'une covariance diagonale avec variances non identiques
        __zero = numpy.zeros(__n)
        __std  = numpy.sqrt(__Covariance.assparsematrix())
        __Ensemble += numpy.asarray([numpy.random.normal(__zero, __std) for i in range(__m)]).T
    #
    elif hasattr(__Covariance,"ismatrix") and __Covariance.ismatrix():
        # Traitement d'une covariance pleine
        __Ensemble += numpy.random.multivariate_normal(numpy.zeros(__n), __Covariance.asfullmatrix(__n), size=__m).T
    #
    elif isinstance(__Covariance, numpy.ndarray):
        # Traitement d'une covariance numpy pleine, sachant qu'on arrive ici en dernier
        __Ensemble += numpy.random.multivariate_normal(numpy.zeros(__n), __Covariance, size=__m).T
    #
    else:
        raise ValueError("Error in ensemble perturbation with inadequate covariance specification")
    #
    return __Ensemble

# ==============================================================================
def CovarianceInflation(
        InputCovOrEns,
        InflationType   = None,
        InflationFactor = None,
        BackgroundCov   = None,
        ):
    """
    Inflation applicable soit sur Pb ou Pa, soit sur les ensembles EXb ou EXa

    Synthèse : Hunt 2007, section 2.3.5
    """
    if InflationFactor is None:
        return InputCovOrEns
    else:
        InflationFactor = float(InflationFactor)
    #
    if InflationType in ["MultiplicativeOnAnalysisCovariance", "MultiplicativeOnBackgroundCovariance"]:
        if InflationFactor < 1.:
            raise ValueError("Inflation factor for multiplicative inflation has to be greater or equal than 1.")
        if InflationFactor < 1.+mpr:
            return InputCovOrEns
        OutputCovOrEns = InflationFactor**2 * InputCovOrEns
    #
    elif InflationType in ["MultiplicativeOnAnalysisAnomalies", "MultiplicativeOnBackgroundAnomalies"]:
        if InflationFactor < 1.:
            raise ValueError("Inflation factor for multiplicative inflation has to be greater or equal than 1.")
        if InflationFactor < 1.+mpr:
            return InputCovOrEns
        InputCovOrEnsMean = InputCovOrEns.mean(axis=1, dtype=mfp).astype('float')
        OutputCovOrEns = InputCovOrEnsMean[:,numpy.newaxis] \
            + InflationFactor * (InputCovOrEns - InputCovOrEnsMean[:,numpy.newaxis])
    #
    elif InflationType in ["AdditiveOnAnalysisCovariance", "AdditiveOnBackgroundCovariance"]:
        if InflationFactor < 0.:
            raise ValueError("Inflation factor for additive inflation has to be greater or equal than 0.")
        if InflationFactor < mpr:
            return InputCovOrEns
        __n, __m = numpy.asarray(InputCovOrEns).shape
        if __n != __m:
            raise ValueError("Additive inflation can only be applied to squared (covariance) matrix.")
        OutputCovOrEns = (1. - InflationFactor) * InputCovOrEns + InflationFactor * numpy.identity(__n)
    #
    elif InflationType == "HybridOnBackgroundCovariance":
        if InflationFactor < 0.:
            raise ValueError("Inflation factor for hybrid inflation has to be greater or equal than 0.")
        if InflationFactor < mpr:
            return InputCovOrEns
        __n, __m = numpy.asarray(InputCovOrEns).shape
        if __n != __m:
            raise ValueError("Additive inflation can only be applied to squared (covariance) matrix.")
        if BackgroundCov is None:
            raise ValueError("Background covariance matrix B has to be given for hybrid inflation.")
        if InputCovOrEns.shape != BackgroundCov.shape:
            raise ValueError("Ensemble covariance matrix has to be of same size than background covariance matrix B.")
        OutputCovOrEns = (1. - InflationFactor) * InputCovOrEns + InflationFactor * BackgroundCov
    #
    elif InflationType == "Relaxation":
        raise NotImplementedError("InflationType Relaxation")
    #
    else:
        raise ValueError("Error in inflation type, '%s' is not a valid keyword."%InflationType)
    #
    return OutputCovOrEns

# ==============================================================================
def HessienneEstimation(nb, HaM, HtM, BI, RI):
    "Estimation de la Hessienne"
    #
    HessienneI = []
    for i in range(int(nb)):
        _ee    = numpy.zeros((nb,1))
        _ee[i] = 1.
        _HtEE  = numpy.dot(HtM,_ee).reshape((-1,1))
        HessienneI.append( numpy.ravel( BI * _ee + HaM * (RI * _HtEE) ) )
    #
    A = numpy.linalg.inv(numpy.array( HessienneI ))
    #
    if min(A.shape) != max(A.shape):
        raise ValueError("The %s a posteriori covariance matrix A is of shape %s, despites it has to be a squared matrix. There is an error in the observation operator, please check it."%(selfA._name,str(A.shape)))
    if (numpy.diag(A) < 0).any():
        raise ValueError("The %s a posteriori covariance matrix A has at least one negative value on its diagonal. There is an error in the observation operator, please check it."%(selfA._name,))
    if logging.getLogger().level < logging.WARNING: # La verification n'a lieu qu'en debug
        try:
            L = numpy.linalg.cholesky( A )
        except:
            raise ValueError("The %s a posteriori covariance matrix A is not symmetric positive-definite. Please check your a priori covariances and your observation operator."%(selfA._name,))
    #
    return A

# ==============================================================================
def QuantilesEstimations(selfA, A, Xa, HXa = None, Hm = None, HtM = None):
    "Estimation des quantiles a posteriori (selfA est modifié)"
    nbsamples = selfA._parameters["NumberOfSamplesForQuantiles"]
    #
    # Traitement des bornes
    if "StateBoundsForQuantiles" in selfA._parameters:
        LBounds = selfA._parameters["StateBoundsForQuantiles"] # Prioritaire
    elif "Bounds" in selfA._parameters:
        LBounds = selfA._parameters["Bounds"]  # Défaut raisonnable
    else:
        LBounds = None
    if LBounds is not None:
        LBounds = ForceNumericBounds( LBounds )
    _Xa = numpy.ravel(Xa)
    #
    # Échantillonnage des états
    YfQ  = None
    EXr  = None
    for i in range(nbsamples):
        if selfA._parameters["SimulationForQuantiles"] == "Linear" and HtM is not None and HXa is not None:
            dXr = (numpy.random.multivariate_normal(_Xa,A) - _Xa).reshape((-1,1))
            if LBounds is not None: # "EstimateProjection" par défaut
                dXr = numpy.max(numpy.hstack((dXr,LBounds[:,0].reshape((-1,1))) - Xa),axis=1)
                dXr = numpy.min(numpy.hstack((dXr,LBounds[:,1].reshape((-1,1))) - Xa),axis=1)
            dYr = HtM @ dXr
            Yr = HXa.reshape((-1,1)) + dYr
            if selfA._toStore("SampledStateForQuantiles"): Xr = _Xa + numpy.ravel(dXr)
        elif selfA._parameters["SimulationForQuantiles"] == "NonLinear" and Hm is not None:
            Xr = numpy.random.multivariate_normal(_Xa,A)
            if LBounds is not None: # "EstimateProjection" par défaut
                Xr = numpy.max(numpy.hstack((Xr.reshape((-1,1)),LBounds[:,0].reshape((-1,1)))),axis=1)
                Xr = numpy.min(numpy.hstack((Xr.reshape((-1,1)),LBounds[:,1].reshape((-1,1)))),axis=1)
            Yr = numpy.asarray(Hm( Xr ))
        else:
            raise ValueError("Quantile simulations has only to be Linear or NonLinear.")
        #
        if YfQ is None:
            YfQ = Yr.reshape((-1,1))
            if selfA._toStore("SampledStateForQuantiles"): EXr = Xr.reshape((-1,1))
        else:
            YfQ = numpy.hstack((YfQ,Yr.reshape((-1,1))))
            if selfA._toStore("SampledStateForQuantiles"): EXr = numpy.hstack((EXr,Xr.reshape((-1,1))))
    #
    # Extraction des quantiles
    YfQ.sort(axis=-1)
    YQ = None
    for quantile in selfA._parameters["Quantiles"]:
        if not (0. <= float(quantile) <= 1.): continue
        indice = int(nbsamples * float(quantile) - 1./nbsamples)
        if YQ is None: YQ = YfQ[:,indice].reshape((-1,1))
        else:          YQ = numpy.hstack((YQ,YfQ[:,indice].reshape((-1,1))))
    if YQ is not None: # Liste non vide de quantiles
        selfA.StoredVariables["SimulationQuantiles"].store( YQ )
    if selfA._toStore("SampledStateForQuantiles"):
        selfA.StoredVariables["SampledStateForQuantiles"].store( EXr )
    #
    return 0

# ==============================================================================
def ForceNumericBounds( __Bounds ):
    "Force les bornes à être des valeurs numériques, sauf si globalement None"
    # Conserve une valeur par défaut à None s'il n'y a pas de bornes
    if __Bounds is None: return None
    # Converti toutes les bornes individuelles None à +/- l'infini
    __Bounds = numpy.asarray( __Bounds, dtype=float )
    if len(__Bounds.shape) != 2 or min(__Bounds.shape) <= 0 or __Bounds.shape[1] != 2:
        raise ValueError("Incorrectly shaped bounds data")
    __Bounds[numpy.isnan(__Bounds[:,0]),0] = -sys.float_info.max
    __Bounds[numpy.isnan(__Bounds[:,1]),1] =  sys.float_info.max
    return __Bounds

# ==============================================================================
def RecentredBounds( __Bounds, __Center):
    "Recentre les bornes autour de 0, sauf si globalement None"
    # Conserve une valeur par défaut à None s'il n'y a pas de bornes
    if __Bounds is None: return None
    # Recentre les valeurs numériques de bornes
    return ForceNumericBounds( __Bounds ) - numpy.ravel( __Center ).reshape((-1,1))

# ==============================================================================
def ApplyBounds( __Vector, __Bounds, __newClip = True):
    "Applique des bornes numériques à un point"
    # Conserve une valeur par défaut s'il n'y a pas de bornes
    if __Bounds is None: return __Vector
    #
    if not isinstance(__Vector, numpy.ndarray): # Is an array
        raise ValueError("Incorrect array definition of vector data")
    if not isinstance(__Bounds, numpy.ndarray): # Is an array
        raise ValueError("Incorrect array definition of bounds data")
    if 2*__Vector.size != __Bounds.size: # Is a 2 column array of vector lenght
        raise ValueError("Incorrect bounds number (%i) to be applied for this vector (of size %i)"%(__Bounds.size,__Vector.size))
    if len(__Bounds.shape) != 2 or min(__Bounds.shape) <= 0 or __Bounds.shape[1] != 2:
        raise ValueError("Incorrectly shaped bounds data")
    #
    if __newClip:
        __Vector = __Vector.clip(
            __Bounds[:,0].reshape(__Vector.shape),
            __Bounds[:,1].reshape(__Vector.shape),
            )
    else:
        __Vector = numpy.max(numpy.hstack((__Vector.reshape((-1,1)),numpy.asmatrix(__Bounds)[:,0])),axis=1)
        __Vector = numpy.min(numpy.hstack((__Vector.reshape((-1,1)),numpy.asmatrix(__Bounds)[:,1])),axis=1)
        __Vector = numpy.asarray(__Vector)
    #
    return __Vector

# ==============================================================================
def Apply3DVarRecentringOnEnsemble(__EnXn, __EnXf, __Ynpu, __HO, __R, __B, __Betaf):
    "Recentre l'ensemble Xn autour de l'analyse 3DVAR"
    #
    Xf = EnsembleMean( __EnXf )
    Pf = Covariance( asCovariance=EnsembleErrorCovariance(__EnXf) )
    Pf = (1 - __Betaf) * __B + __Betaf * Pf
    #
    selfB = PartialAlgorithm("3DVAR")
    selfB._parameters["Minimizer"] = "LBFGSB"
    selfB._parameters["MaximumNumberOfSteps"] = 15000
    selfB._parameters["CostDecrementTolerance"] = 1.e-7
    selfB._parameters["ProjectedGradientTolerance"] = -1
    selfB._parameters["GradientNormTolerance"] = 1.e-05
    selfB._parameters["StoreInternalVariables"] = False
    selfB._parameters["optiprint"] = -1
    selfB._parameters["optdisp"] = 0
    selfB._parameters["Bounds"] = None
    selfB._parameters["InitializationPoint"] = Xf
    std3dvar(selfB, Xf, __Ynpu, None, __HO, None, None, __R, Pf, None)
    Xa = selfB.get("Analysis")[-1].reshape((-1,1))
    del selfB
    #
    return Xa + EnsembleOfAnomalies( __EnXn )

# ==============================================================================
def c2ukf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    Constrained Unscented Kalman Filter
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    selfA._parameters["Bounds"] = ForceNumericBounds( selfA._parameters["Bounds"] )
    #
    L     = Xb.size
    Alpha = selfA._parameters["Alpha"]
    Beta  = selfA._parameters["Beta"]
    if selfA._parameters["Kappa"] == 0:
        if selfA._parameters["EstimationOf"] == "State":
            Kappa = 0
        elif selfA._parameters["EstimationOf"] == "Parameters":
            Kappa = 3 - L
    else:
        Kappa = selfA._parameters["Kappa"]
    Lambda = float( Alpha**2 ) * ( L + Kappa ) - L
    Gamma  = math.sqrt( L + Lambda )
    #
    Ww = []
    Ww.append( 0. )
    for i in range(2*L):
        Ww.append( 1. / (2.*(L + Lambda)) )
    #
    Wm = numpy.array( Ww )
    Wm[0] = Lambda / (L + Lambda)
    Wc = numpy.array( Ww )
    Wc[0] = Lambda / (L + Lambda) + (1. - Alpha**2 + Beta)
    #
    # Opérateurs
    Hm = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
        Mm = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    # Durée d'observation et tailles
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
        __p = numpy.cumprod(Y.shape())[-1]
    else:
        duration = 2
        __p = numpy.array(Y).size
    #
    # Précalcul des inversions de B et R
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
        RI = R.getI()
    #
    __n = Xb.size
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        Xn = Xb
        if hasattr(B,"asfullmatrix"):
            Pn = B.asfullmatrix(__n)
        else:
            Pn = B
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
        Pn = selfA._getInternalState("Pn")
    #
    if selfA._parameters["EstimationOf"] == "Parameters":
        XaMin            = Xn
        previousJMinimum = numpy.finfo(float).max
    #
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        Pndemi = numpy.real(scipy.linalg.sqrtm(Pn))
        Xnp = numpy.hstack([Xn, Xn+Gamma*Pndemi, Xn-Gamma*Pndemi])
        nbSpts = 2*Xn.size+1
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            for point in range(nbSpts):
                Xnp[:,point] = ApplyBounds( Xnp[:,point], selfA._parameters["Bounds"] )
        #
        XEtnnp = []
        for point in range(nbSpts):
            if selfA._parameters["EstimationOf"] == "State":
                XEtnnpi = numpy.asarray( Mm( (Xnp[:,point], Un) ) ).reshape((-1,1))
                if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                    Cm = Cm.reshape(Xn.size,Un.size) # ADAO & check shape
                    XEtnnpi = XEtnnpi + Cm @ Un
                if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
                    XEtnnpi = ApplyBounds( XEtnnpi, selfA._parameters["Bounds"] )
            elif selfA._parameters["EstimationOf"] == "Parameters":
                # --- > Par principe, M = Id, Q = 0
                XEtnnpi = Xnp[:,point]
            XEtnnp.append( numpy.ravel(XEtnnpi).reshape((-1,1)) )
        XEtnnp = numpy.concatenate( XEtnnp, axis=1 )
        #
        Xncm = ( XEtnnp * Wm ).sum(axis=1)
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            Xncm = ApplyBounds( Xncm, selfA._parameters["Bounds"] )
        #
        if selfA._parameters["EstimationOf"] == "State":        Pnm = Q
        elif selfA._parameters["EstimationOf"] == "Parameters": Pnm = 0.
        for point in range(nbSpts):
            Pnm += Wc[i] * ((XEtnnp[:,point]-Xncm).reshape((-1,1)) * (XEtnnp[:,point]-Xncm))
        #
        if selfA._parameters["EstimationOf"] == "Parameters" and selfA._parameters["Bounds"] is not None:
            Pnmdemi = selfA._parameters["Reconditioner"] * numpy.real(scipy.linalg.sqrtm(Pnm))
        else:
            Pnmdemi = numpy.real(scipy.linalg.sqrtm(Pnm))
        #
        Xnnp = numpy.hstack([Xncm.reshape((-1,1)), Xncm.reshape((-1,1))+Gamma*Pnmdemi, Xncm.reshape((-1,1))-Gamma*Pnmdemi])
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            for point in range(nbSpts):
                Xnnp[:,point] = ApplyBounds( Xnnp[:,point], selfA._parameters["Bounds"] )
        #
        Ynnp = []
        for point in range(nbSpts):
            if selfA._parameters["EstimationOf"] == "State":
                Ynnpi = Hm( (Xnnp[:,point], None) )
            elif selfA._parameters["EstimationOf"] == "Parameters":
                Ynnpi = Hm( (Xnnp[:,point], Un) )
            Ynnp.append( numpy.ravel(Ynnpi).reshape((-1,1)) )
        Ynnp = numpy.concatenate( Ynnp, axis=1 )
        #
        Yncm = ( Ynnp * Wm ).sum(axis=1)
        #
        Pyyn = R
        Pxyn = 0.
        for point in range(nbSpts):
            Pyyn += Wc[i] * ((Ynnp[:,point]-Yncm).reshape((-1,1)) * (Ynnp[:,point]-Yncm))
            Pxyn += Wc[i] * ((Xnnp[:,point]-Xncm).reshape((-1,1)) * (Ynnp[:,point]-Yncm))
        #
        _Innovation  = Ynpu - Yncm.reshape((-1,1))
        if selfA._parameters["EstimationOf"] == "Parameters":
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans H, doublon !
                _Innovation = _Innovation - Cm @ Un
        #
        Kn = Pxyn * Pyyn.I
        Xn = Xncm.reshape((-1,1)) + Kn * _Innovation
        Pn = Pnm - Kn * Pyyn * Kn.T
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            Xn = ApplyBounds( Xn, selfA._parameters["Bounds"] )
        #
        Xa = Xn # Pointeurs
        #--------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("Pn", Pn)
        #--------------------------
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( Hm((Xa, Un)) )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( Xncm )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( Pnm )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( Xncm - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( Yncm )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T * (BI * (Xa - Xb)) )
            Jo  = float( 0.5 * _Innovation.T * (RI * _Innovation) )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = selfA.StoredVariables["APosterioriCovariance"][-1]
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def cekf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    Contrained Extended Kalman Filter
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    selfA._parameters["Bounds"] = ForceNumericBounds( selfA._parameters["Bounds"] )
    #
    # Opérateurs
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
        M = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    # Durée d'observation et tailles
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
        __p = numpy.cumprod(Y.shape())[-1]
    else:
        duration = 2
        __p = numpy.array(Y).size
    #
    # Précalcul des inversions de B et R
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
        RI = R.getI()
    #
    __n = Xb.size
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        Xn = Xb
        Pn = B
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            if hasattr(B,"asfullmatrix"):
                selfA.StoredVariables["APosterioriCovariance"].store( B.asfullmatrix(__n) )
            else:
                selfA.StoredVariables["APosterioriCovariance"].store( B )
        selfA._setInternalState("seed", numpy.random.get_state())
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
        Pn = selfA._getInternalState("Pn")
    #
    if selfA._parameters["EstimationOf"] == "Parameters":
        XaMin            = Xn
        previousJMinimum = numpy.finfo(float).max
    #
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        #
        Ht = HO["Tangent"].asMatrix(ValueForMethodForm = Xn)
        Ht = Ht.reshape(Ynpu.size,Xn.size) # ADAO & check shape
        Ha = HO["Adjoint"].asMatrix(ValueForMethodForm = Xn)
        Ha = Ha.reshape(Xn.size,Ynpu.size) # ADAO & check shape
        #
        if selfA._parameters["EstimationOf"] == "State":
            Mt = EM["Tangent"].asMatrix(ValueForMethodForm = Xn)
            Mt = Mt.reshape(Xn.size,Xn.size) # ADAO & check shape
            Ma = EM["Adjoint"].asMatrix(ValueForMethodForm = Xn)
            Ma = Ma.reshape(Xn.size,Xn.size) # ADAO & check shape
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            Xn = ApplyBounds( Xn, selfA._parameters["Bounds"] )
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast + Q and observation of forecast
            Xn_predicted = numpy.ravel( M( (Xn, Un) ) ).reshape((__n,1))
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm @ Un
            Pn_predicted = Q + Mt * (Pn * Ma)
        elif selfA._parameters["EstimationOf"] == "Parameters": # Observation of forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = Xn
            Pn_predicted = Pn
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            Xn_predicted = ApplyBounds( Xn_predicted, selfA._parameters["Bounds"] )
        #
        if selfA._parameters["EstimationOf"] == "State":
            HX_predicted = numpy.ravel( H( (Xn_predicted, None) ) ).reshape((__p,1))
            _Innovation  = Ynpu - HX_predicted
        elif selfA._parameters["EstimationOf"] == "Parameters":
            HX_predicted = numpy.ravel( H( (Xn_predicted, Un) ) ).reshape((__p,1))
            _Innovation  = Ynpu - HX_predicted
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans H, doublon !
                _Innovation = _Innovation - Cm @ Un
        #
        Kn = Pn_predicted * Ha * numpy.linalg.inv(R + numpy.dot(Ht, Pn_predicted * Ha))
        Xn = Xn_predicted + Kn * _Innovation
        Pn = Pn_predicted - Kn * Ht * Pn_predicted
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            Xn = ApplyBounds( Xn, selfA._parameters["Bounds"] )
        #
        Xa = Xn # Pointeurs
        #--------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("Pn", Pn)
        #--------------------------
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( H((Xa, Un)) )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( Xn_predicted )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( Pn_predicted )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( Xn_predicted - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HX_predicted )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T @ (BI @ (Xa - Xb)) )
            Jo  = float( 0.5 * _Innovation.T @ (RI @ _Innovation) )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = selfA.StoredVariables["APosterioriCovariance"][-1]
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def enks(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="EnKS16-KalmanFilterFormula"):
    """
    EnKS
    """
    #
    # Opérateurs
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
        M = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    # Précalcul des inversions de B et R
    RIdemi = R.sqrtmI()
    #
    # Durée d'observation et tailles
    LagL = selfA._parameters["SmootherLagL"]
    if (not hasattr(Y,"store")) or (not hasattr(Y,"stepnumber")):
        raise ValueError("Fixed-lag smoother requires a series of observation")
    if Y.stepnumber() < LagL:
        raise ValueError("Fixed-lag smoother requires a series of observation greater then the lag L")
    duration = Y.stepnumber()
    __p = numpy.cumprod(Y.shape())[-1]
    __n = Xb.size
    __m = selfA._parameters["NumberOfMembers"]
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            if hasattr(B,"asfullmatrix"):
                selfA.StoredVariables["APosterioriCovariance"].store( B.asfullmatrix(__n) )
            else:
                selfA.StoredVariables["APosterioriCovariance"].store( B )
    #
    # Calcul direct initial (on privilégie la mémorisation au recalcul)
    __seed = numpy.random.get_state()
    selfB = copy.deepcopy(selfA)
    selfB._parameters["StoreSupplementaryCalculations"] = ["CurrentEnsembleState"]
    if VariantM == "EnKS16-KalmanFilterFormula":
        etkf(selfB, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM = "KalmanFilterFormula")
    else:
        raise ValueError("VariantM has to be chosen in the authorized methods list.")
    if LagL > 0:
        EL  = selfB.StoredVariables["CurrentEnsembleState"][LagL-1]
    else:
        EL = EnsembleOfBackgroundPerturbations( Xb, None, __m ) # Cf. etkf
    selfA._parameters["SetSeed"] = numpy.random.set_state(__seed)
    #
    for step in range(LagL,duration-1):
        #
        sEL = selfB.StoredVariables["CurrentEnsembleState"][step+1-LagL:step+1]
        sEL.append(None)
        #
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        #--------------------------
        if VariantM == "EnKS16-KalmanFilterFormula":
            if selfA._parameters["EstimationOf"] == "State": # Forecast
                EL = M( [(EL[:,i], Un) for i in range(__m)],
                    argsAsSerie = True,
                    returnSerieAsArrayMatrix = True )
                EL = EnsemblePerturbationWithGivenCovariance( EL, Q )
                EZ = H( [(EL[:,i], Un) for i in range(__m)],
                    argsAsSerie = True,
                    returnSerieAsArrayMatrix = True )
                if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                    Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                    EZ = EZ + Cm @ Un
            elif selfA._parameters["EstimationOf"] == "Parameters":
                # --- > Par principe, M = Id, Q = 0
                EZ = H( [(EL[:,i], Un) for i in range(__m)],
                    argsAsSerie = True,
                    returnSerieAsArrayMatrix = True )
            #
            vEm   = EL.mean(axis=1, dtype=mfp).astype('float').reshape((__n,1))
            vZm   = EZ.mean(axis=1, dtype=mfp).astype('float').reshape((__p,1))
            #
            mS    = RIdemi @ EnsembleOfAnomalies( EZ, vZm, 1./math.sqrt(__m-1) )
            mS    = mS.reshape((-1,__m)) # Pour dimension 1
            delta = RIdemi @ ( Ynpu - vZm )
            mT    = numpy.linalg.inv( numpy.identity(__m) + mS.T @ mS )
            vw    = mT @ mS.T @ delta
            #
            Tdemi = numpy.real(scipy.linalg.sqrtm(mT))
            mU    = numpy.identity(__m)
            wTU   = (vw.reshape((__m,1)) + math.sqrt(__m-1) * Tdemi @ mU)
            #
            EX    = EnsembleOfAnomalies( EL, vEm, 1./math.sqrt(__m-1) )
            EL    = vEm + EX @ wTU
            #
            sEL[LagL] = EL
            for irl in range(LagL): # Lissage des L précédentes analysis
                vEm = sEL[irl].mean(axis=1, dtype=mfp).astype('float').reshape((__n,1))
                EX = EnsembleOfAnomalies( sEL[irl], vEm, 1./math.sqrt(__m-1) )
                sEL[irl] = vEm + EX @ wTU
            #
            # Conservation de l'analyse retrospective d'ordre 0 avant rotation
            Xa = sEL[0].mean(axis=1, dtype=mfp).astype('float').reshape((__n,1))
            if selfA._toStore("APosterioriCovariance"):
                EXn = sEL[0]
            #
            for irl in range(LagL):
                sEL[irl] = sEL[irl+1]
            sEL[LagL] = None
        #--------------------------
        else:
            raise ValueError("VariantM has to be chosen in the authorized methods list.")
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( EnsembleErrorCovariance(EXn) )
    #
    # Stockage des dernières analyses incomplètement remises à jour
    for irl in range(LagL):
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        Xa = sEL[irl].mean(axis=1, dtype=mfp).astype('float').reshape((__n,1))
        selfA.StoredVariables["Analysis"].store( Xa )
    #
    return 0

# ==============================================================================
def etkf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q,
    VariantM="KalmanFilterFormula",
    Hybrid=None,
    ):
    """
    Ensemble-Transform EnKF
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Opérateurs
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
        M = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    # Durée d'observation et tailles
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
        __p = numpy.cumprod(Y.shape())[-1]
    else:
        duration = 2
        __p = numpy.array(Y).size
    #
    # Précalcul des inversions de B et R
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
        RI = R.getI()
    elif VariantM != "KalmanFilterFormula":
        RI = R.getI()
    if VariantM == "KalmanFilterFormula":
        RIdemi = R.sqrtmI()
    #
    __n = Xb.size
    __m = selfA._parameters["NumberOfMembers"]
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    previousJMinimum = numpy.finfo(float).max
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        Xn = EnsembleOfBackgroundPerturbations( Xb, None, __m )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            if hasattr(B,"asfullmatrix"):
                selfA.StoredVariables["APosterioriCovariance"].store( B.asfullmatrix(__n) )
            else:
                selfA.StoredVariables["APosterioriCovariance"].store( B )
        selfA._setInternalState("seed", numpy.random.get_state())
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
    #
    for step in range(duration-1):
        numpy.random.set_state(selfA._getInternalState("seed"))
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnBackgroundAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast + Q and observation of forecast
            EMX = M( [(Xn[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
            Xn_predicted = EnsemblePerturbationWithGivenCovariance( EMX, Q )
            HX_predicted = H( [(Xn_predicted[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm @ Un
        elif selfA._parameters["EstimationOf"] == "Parameters": # Observation of forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = EMX = Xn
            HX_predicted = H( [(Xn_predicted[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
        #
        # Mean of forecast and observation of forecast
        Xfm  = EnsembleMean( Xn_predicted )
        Hfm  = EnsembleMean( HX_predicted )
        #
        # Anomalies
        EaX   = EnsembleOfAnomalies( Xn_predicted, Xfm )
        EaHX  = EnsembleOfAnomalies( HX_predicted, Hfm)
        #
        #--------------------------
        if VariantM == "KalmanFilterFormula":
            mS    = RIdemi * EaHX / math.sqrt(__m-1)
            mS    = mS.reshape((-1,__m)) # Pour dimension 1
            delta = RIdemi * ( Ynpu - Hfm )
            mT    = numpy.linalg.inv( numpy.identity(__m) + mS.T @ mS )
            vw    = mT @ mS.T @ delta
            #
            Tdemi = numpy.real(scipy.linalg.sqrtm(mT))
            mU    = numpy.identity(__m)
            #
            EaX   = EaX / math.sqrt(__m-1)
            Xn    = Xfm + EaX @ ( vw.reshape((__m,1)) + math.sqrt(__m-1) * Tdemi @ mU )
        #--------------------------
        elif VariantM == "Variational":
            HXfm = H((Xfm[:,None], Un)) # Eventuellement Hfm
            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,1)) - (EaHX @ w).reshape((__p,1))
                _Jo = 0.5 * _A.T @ (RI * _A)
                _Jb = 0.5 * (__m-1) * w.T @ w
                _J  = _Jo + _Jb
                return float(_J)
            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,1)) - (EaHX @ w).reshape((__p,1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = (__m-1) * w.reshape((__m,1))
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)
            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
                )
            #
            Hto = EaHX.T @ (RI * EaHX).reshape((-1,__m))
            Htb = (__m-1) * numpy.identity(__m)
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m-1)*Pta)) # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw[:,None] + EWa)
        #--------------------------
        elif VariantM == "FiniteSize11": # Jauge Boc2011
            HXfm = H((Xfm[:,None], Un)) # Eventuellement Hfm
            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,1)) - (EaHX @ w).reshape((__p,1))
                _Jo = 0.5 * _A.T @ (RI * _A)
                _Jb = 0.5 * __m * math.log(1 + 1/__m + w.T @ w)
                _J  = _Jo + _Jb
                return float(_J)
            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,1)) - (EaHX @ w).reshape((__p,1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = __m * w.reshape((__m,1)) / (1 + 1/__m + w.T @ w)
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)
            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
                )
            #
            Hto = EaHX.T @ (RI * EaHX).reshape((-1,__m))
            Htb = __m * \
                ( (1 + 1/__m + vw.T @ vw) * numpy.identity(__m) - 2 * vw @ vw.T ) \
                / (1 + 1/__m + vw.T @ vw)**2
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m-1)*Pta)) # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw.reshape((__m,1)) + EWa)
        #--------------------------
        elif VariantM == "FiniteSize15": # Jauge Boc2015
            HXfm = H((Xfm[:,None], Un)) # Eventuellement Hfm
            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,1)) - (EaHX @ w).reshape((__p,1))
                _Jo = 0.5 * _A.T * (RI * _A)
                _Jb = 0.5 * (__m+1) * math.log(1 + 1/__m + w.T @ w)
                _J  = _Jo + _Jb
                return float(_J)
            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,1)) - (EaHX @ w).reshape((__p,1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = (__m+1) * w.reshape((__m,1)) / (1 + 1/__m + w.T @ w)
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)
            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
                )
            #
            Hto = EaHX.T @ (RI * EaHX).reshape((-1,__m))
            Htb = (__m+1) * \
                ( (1 + 1/__m + vw.T @ vw) * numpy.identity(__m) - 2 * vw @ vw.T ) \
                / (1 + 1/__m + vw.T @ vw)**2
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m-1)*Pta)) # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw.reshape((__m,1)) + EWa)
        #--------------------------
        elif VariantM == "FiniteSize16": # Jauge Boc2016
            HXfm = H((Xfm[:,None], Un)) # Eventuellement Hfm
            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,1)) - (EaHX @ w).reshape((__p,1))
                _Jo = 0.5 * _A.T @ (RI * _A)
                _Jb = 0.5 * (__m+1) * math.log(1 + 1/__m + w.T @ w / (__m-1))
                _J  = _Jo + _Jb
                return float(_J)
            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,1)) - (EaHX @ w).reshape((__p,1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = ((__m+1) / (__m-1)) * w.reshape((__m,1)) / (1 + 1/__m + w.T @ w / (__m-1))
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)
            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
                )
            #
            Hto = EaHX.T @ (RI * EaHX).reshape((-1,__m))
            Htb = ((__m+1) / (__m-1)) * \
                ( (1 + 1/__m + vw.T @ vw / (__m-1)) * numpy.identity(__m) - 2 * vw @ vw.T / (__m-1) ) \
                / (1 + 1/__m + vw.T @ vw / (__m-1))**2
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m-1)*Pta)) # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw[:,None] + EWa)
        #--------------------------
        else:
            raise ValueError("VariantM has to be chosen in the authorized methods list.")
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnAnalysisAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        if Hybrid == "E3DVAR":
            betaf = selfA._parameters["HybridCovarianceEquilibrium"]
            Xn = Apply3DVarRecentringOnEnsemble(Xn, EMX, Ynpu, HO, R, B, betaf)
        #
        Xa = EnsembleMean( Xn )
        #--------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("seed", numpy.random.get_state())
        #--------------------------
        #
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("APosterioriCovariance") \
            or selfA._toStore("InnovationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            _HXa = numpy.ravel( H((Xa, Un)) ).reshape((-1,1))
            _Innovation = Ynpu - _HXa
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( _HXa )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( EMX )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( EnsembleErrorCovariance(EMX) )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( EMX - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( - HX_predicted + Ynpu )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HX_predicted )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T * (BI * (Xa - Xb)) )
            Jo  = float( 0.5 * _Innovation.T * (RI * _Innovation) )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( EnsembleErrorCovariance(Xn) )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = selfA.StoredVariables["APosterioriCovariance"][-1]
        # ---> Pour les smoothers
        if selfA._toStore("CurrentEnsembleState"):
            selfA.StoredVariables["CurrentEnsembleState"].store( Xn )
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def exkf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    Extended Kalman Filter
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Opérateurs
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
        M = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    # Durée d'observation et tailles
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
        __p = numpy.cumprod(Y.shape())[-1]
    else:
        duration = 2
        __p = numpy.array(Y).size
    #
    # Précalcul des inversions de B et R
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
        RI = R.getI()
    #
    __n = Xb.size
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        Xn = Xb
        Pn = B
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            if hasattr(B,"asfullmatrix"):
                selfA.StoredVariables["APosterioriCovariance"].store( B.asfullmatrix(__n) )
            else:
                selfA.StoredVariables["APosterioriCovariance"].store( B )
        selfA._setInternalState("seed", numpy.random.get_state())
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
        Pn = selfA._getInternalState("Pn")
    #
    if selfA._parameters["EstimationOf"] == "Parameters":
        XaMin            = Xn
        previousJMinimum = numpy.finfo(float).max
    #
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        #
        Ht = HO["Tangent"].asMatrix(ValueForMethodForm = Xn)
        Ht = Ht.reshape(Ynpu.size,Xn.size) # ADAO & check shape
        Ha = HO["Adjoint"].asMatrix(ValueForMethodForm = Xn)
        Ha = Ha.reshape(Xn.size,Ynpu.size) # ADAO & check shape
        #
        if selfA._parameters["EstimationOf"] == "State":
            Mt = EM["Tangent"].asMatrix(ValueForMethodForm = Xn)
            Mt = Mt.reshape(Xn.size,Xn.size) # ADAO & check shape
            Ma = EM["Adjoint"].asMatrix(ValueForMethodForm = Xn)
            Ma = Ma.reshape(Xn.size,Xn.size) # ADAO & check shape
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast + Q and observation of forecast
            Xn_predicted = numpy.ravel( M( (Xn, Un) ) ).reshape((__n,1))
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm @ Un
            Pn_predicted = Q + Mt * (Pn * Ma)
        elif selfA._parameters["EstimationOf"] == "Parameters": # Observation of forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = Xn
            Pn_predicted = Pn
        #
        if selfA._parameters["EstimationOf"] == "State":
            HX_predicted = numpy.ravel( H( (Xn_predicted, None) ) ).reshape((__p,1))
            _Innovation  = Ynpu - HX_predicted
        elif selfA._parameters["EstimationOf"] == "Parameters":
            HX_predicted = numpy.ravel( H( (Xn_predicted, Un) ) ).reshape((__p,1))
            _Innovation  = Ynpu - HX_predicted
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans H, doublon !
                _Innovation = _Innovation - Cm @ Un
        #
        Kn = Pn_predicted * Ha * numpy.linalg.inv(R + numpy.dot(Ht, Pn_predicted * Ha))
        Xn = Xn_predicted + Kn * _Innovation
        Pn = Pn_predicted - Kn * Ht * Pn_predicted
        #
        Xa = Xn # Pointeurs
        #--------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("Pn", Pn)
        #--------------------------
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( H((Xa, Un)) )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( Xn_predicted )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( Pn_predicted )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( Xn_predicted - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HX_predicted )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T @ (BI @ (Xa - Xb)) )
            Jo  = float( 0.5 * _Innovation.T @ (RI @ _Innovation) )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = selfA.StoredVariables["APosterioriCovariance"][-1]
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def ienkf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="IEnKF12",
    BnotT=False, _epsilon=1.e-3, _e=1.e-7, _jmax=15000):
    """
    Iterative EnKF
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Opérateurs
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
        M = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    # Durée d'observation et tailles
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
        __p = numpy.cumprod(Y.shape())[-1]
    else:
        duration = 2
        __p = numpy.array(Y).size
    #
    # Précalcul des inversions de B et R
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
    RI = R.getI()
    #
    __n = Xb.size
    __m = selfA._parameters["NumberOfMembers"]
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    previousJMinimum = numpy.finfo(float).max
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        if hasattr(B,"asfullmatrix"): Pn = B.asfullmatrix(__n)
        else:                         Pn = B
        Xn = EnsembleOfBackgroundPerturbations( Xb, Pn, __m )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            if hasattr(B,"asfullmatrix"):
                selfA.StoredVariables["APosterioriCovariance"].store( B.asfullmatrix(__n) )
            else:
                selfA.StoredVariables["APosterioriCovariance"].store( B )
        selfA._setInternalState("seed", numpy.random.get_state())
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
    #
    for step in range(duration-1):
        numpy.random.set_state(selfA._getInternalState("seed"))
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnBackgroundAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        #--------------------------
        if VariantM == "IEnKF12":
            Xfm = numpy.ravel(Xn.mean(axis=1, dtype=mfp).astype('float'))
            EaX = EnsembleOfAnomalies( Xn ) / math.sqrt(__m-1)
            __j = 0
            Deltaw = 1
            if not BnotT:
                Ta  = numpy.identity(__m)
            vw  = numpy.zeros(__m)
            while numpy.linalg.norm(Deltaw) >= _e and __j <= _jmax:
                vx1 = (Xfm + EaX @ vw).reshape((__n,1))
                #
                if BnotT:
                    E1 = vx1 + _epsilon * EaX
                else:
                    E1 = vx1 + math.sqrt(__m-1) * EaX @ Ta
                #
                if selfA._parameters["EstimationOf"] == "State": # Forecast + Q
                    E2 = M( [(E1[:,i,numpy.newaxis], Un) for i in range(__m)],
                        argsAsSerie = True,
                        returnSerieAsArrayMatrix = True )
                elif selfA._parameters["EstimationOf"] == "Parameters":
                    # --- > Par principe, M = Id
                    E2 = Xn
                vx2 = E2.mean(axis=1, dtype=mfp).astype('float').reshape((__n,1))
                vy1 = H((vx2, Un)).reshape((__p,1))
                #
                HE2 = H( [(E2[:,i,numpy.newaxis], Un) for i in range(__m)],
                    argsAsSerie = True,
                    returnSerieAsArrayMatrix = True )
                vy2 = HE2.mean(axis=1, dtype=mfp).astype('float').reshape((__p,1))
                #
                if BnotT:
                    EaY = (HE2 - vy2) / _epsilon
                else:
                    EaY = ( (HE2 - vy2) @ numpy.linalg.inv(Ta) ) / math.sqrt(__m-1)
                #
                GradJ = numpy.ravel(vw[:,None] - EaY.transpose() @ (RI * ( Ynpu - vy1 )))
                mH = numpy.identity(__m) + EaY.transpose() @ (RI * EaY).reshape((-1,__m))
                Deltaw = - numpy.linalg.solve(mH,GradJ)
                #
                vw = vw + Deltaw
                #
                if not BnotT:
                    Ta = numpy.real(scipy.linalg.sqrtm(numpy.linalg.inv( mH )))
                #
                __j = __j + 1
            #
            A2 = EnsembleOfAnomalies( E2 )
            #
            if BnotT:
                Ta = numpy.real(scipy.linalg.sqrtm(numpy.linalg.inv( mH )))
                A2 = math.sqrt(__m-1) * A2 @ Ta / _epsilon
            #
            Xn = vx2 + A2
        #--------------------------
        else:
            raise ValueError("VariantM has to be chosen in the authorized methods list.")
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnAnalysisAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        Xa = EnsembleMean( Xn )
        #--------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("seed", numpy.random.get_state())
        #--------------------------
        #
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("APosterioriCovariance") \
            or selfA._toStore("InnovationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            _HXa = numpy.ravel( H((Xa, Un)) ).reshape((-1,1))
            _Innovation = Ynpu - _HXa
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( _HXa )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( E2 )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( EnsembleErrorCovariance(E2) )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( E2 - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( - HE2 + Ynpu )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HE2 )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T * (BI * (Xa - Xb)) )
            Jo  = float( 0.5 * _Innovation.T * (RI * _Innovation) )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( EnsembleErrorCovariance(Xn) )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = selfA.StoredVariables["APosterioriCovariance"][-1]
        # ---> Pour les smoothers
        if selfA._toStore("CurrentEnsembleState"):
            selfA.StoredVariables["CurrentEnsembleState"].store( Xn )
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def incr3dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    3DVAR incrémental
    """
    #
    # Initialisations
    # ---------------
    Hm = HO["Direct"].appliedTo
    #
    BI = B.getI()
    RI = R.getI()
    #
    HXb = numpy.asarray(Hm( Xb )).reshape((-1,1))
    Innovation = Y - HXb
    #
    # Outer Loop
    # ----------
    iOuter = 0
    J      = 1./mpr
    DeltaJ = 1./mpr
    Xr     = numpy.asarray(selfA._parameters["InitializationPoint"]).reshape((-1,1))
    while abs(DeltaJ) >= selfA._parameters["CostDecrementTolerance"] and iOuter <= selfA._parameters["MaximumNumberOfSteps"]:
        #
        # Inner Loop
        # ----------
        Ht = HO["Tangent"].asMatrix(Xr)
        Ht = Ht.reshape(Y.size,Xr.size) # ADAO & check shape
        #
        # Définition de la fonction-coût
        # ------------------------------
        def CostFunction(dx):
            _dX  = numpy.asarray(dx).reshape((-1,1))
            if selfA._parameters["StoreInternalVariables"] or \
                selfA._toStore("CurrentState") or \
                selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentState"].store( Xb + _dX )
            _HdX = (Ht @ _dX).reshape((-1,1))
            _dInnovation = Innovation - _HdX
            if selfA._toStore("SimulatedObservationAtCurrentState") or \
                selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HXb + _HdX )
            if selfA._toStore("InnovationAtCurrentState"):
                selfA.StoredVariables["InnovationAtCurrentState"].store( _dInnovation )
            #
            Jb  = float( 0.5 * _dX.T * (BI * _dX) )
            Jo  = float( 0.5 * _dInnovation.T * (RI * _dInnovation) )
            J   = Jb + Jo
            #
            selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            if selfA._toStore("IndexOfOptimum") or \
                selfA._toStore("CurrentOptimum") or \
                selfA._toStore("CostFunctionJAtCurrentOptimum") or \
                selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
                selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
                selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["CurrentState"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
            return J
        #
        def GradientOfCostFunction(dx):
            _dX          = numpy.ravel( dx )
            _HdX         = (Ht @ _dX).reshape((-1,1))
            _dInnovation = Innovation - _HdX
            GradJb       = BI @ _dX
            GradJo       = - Ht.T @ (RI * _dInnovation)
            GradJ        = numpy.ravel( GradJb ) + numpy.ravel( GradJo )
            return GradJ
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
        #
        if selfA._parameters["Minimizer"] == "LBFGSB":
            # Minimum, J_optimal, Informations = scipy.optimize.fmin_l_bfgs_b(
            if "0.19" <= scipy.version.version <= "1.1.0":
                import lbfgsbhlt as optimiseur
            else:
                import scipy.optimize as optimiseur
            Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
                func        = CostFunction,
                x0          = numpy.zeros(Xb.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = RecentredBounds(selfA._parameters["Bounds"], Xb),
                maxfun      = selfA._parameters["MaximumNumberOfSteps"]-1,
                factr       = selfA._parameters["CostDecrementTolerance"]*1.e14,
                pgtol       = selfA._parameters["ProjectedGradientTolerance"],
                iprint      = selfA._parameters["optiprint"],
                )
            nfeval = Informations['funcalls']
            rc     = Informations['warnflag']
        elif selfA._parameters["Minimizer"] == "TNC":
            Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
                func        = CostFunction,
                x0          = numpy.zeros(Xb.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = RecentredBounds(selfA._parameters["Bounds"], Xb),
                maxfun      = selfA._parameters["MaximumNumberOfSteps"],
                pgtol       = selfA._parameters["ProjectedGradientTolerance"],
                ftol        = selfA._parameters["CostDecrementTolerance"],
                messages    = selfA._parameters["optmessages"],
                )
        elif selfA._parameters["Minimizer"] == "CG":
            Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(Xb.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = selfA._parameters["MaximumNumberOfSteps"],
                gtol        = selfA._parameters["GradientNormTolerance"],
                disp        = selfA._parameters["optdisp"],
                full_output = True,
                )
        elif selfA._parameters["Minimizer"] == "NCG":
            Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
                f           = CostFunction,
                x0          = numpy.zeros(Xb.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = selfA._parameters["MaximumNumberOfSteps"],
                avextol     = selfA._parameters["CostDecrementTolerance"],
                disp        = selfA._parameters["optdisp"],
                full_output = True,
                )
        elif selfA._parameters["Minimizer"] == "BFGS":
            Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
                f           = CostFunction,
                x0          = numpy.zeros(Xb.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = selfA._parameters["MaximumNumberOfSteps"],
                gtol        = selfA._parameters["GradientNormTolerance"],
                disp        = selfA._parameters["optdisp"],
                full_output = True,
                )
        else:
            raise ValueError("Error in Minimizer name: %s"%selfA._parameters["Minimizer"])
        #
        IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        MinJ     = selfA.StoredVariables["CostFunctionJ"][IndexMin]
        #
        if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
            Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
        else:
            Minimum = Xb + Minimum.reshape((-1,1))
        #
        Xr     = Minimum
        DeltaJ = selfA.StoredVariables["CostFunctionJ" ][-1] - J
        iOuter = selfA.StoredVariables["CurrentIterationNumber"][-1]
    #
    Xa = Xr
    #--------------------------
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    if selfA._toStore("OMA") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm( Xa )
    #
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("JacobianMatrixAtOptimum") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HtM = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
        HtM = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HaM = HO["Adjoint"].asMatrix(ValueForMethodForm = Xa)
        HaM = HaM.reshape(Xa.size,Y.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles"):
        A = HessienneEstimation(Xa.size, HaM, HtM, BI, RI)
    if selfA._toStore("APosterioriCovariance"):
        selfA.StoredVariables["APosterioriCovariance"].store( A )
    if selfA._toStore("JacobianMatrixAtOptimum"):
        selfA.StoredVariables["JacobianMatrixAtOptimum"].store( HtM )
    if selfA._toStore("KalmanGainAtOptimum"):
        if   (Y.size <= Xb.size): KG  = B * HaM * (R + numpy.dot(HtM, B * HaM)).I
        elif (Y.size >  Xb.size): KG = (BI + numpy.dot(HaM, RI * HtM)).I * HaM * RI
        selfA.StoredVariables["KalmanGainAtOptimum"].store( KG )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("Innovation") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("MahalanobisConsistency") or \
        selfA._toStore("OMB"):
        d  = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( d )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( d )
    if selfA._toStore("SigmaObs2"):
        TraceR = R.trace(Y.size)
        selfA.StoredVariables["SigmaObs2"].store( float( (d.T @ (numpy.ravel(Y)-numpy.ravel(HXa))) ) / TraceR )
    if selfA._toStore("MahalanobisConsistency"):
        selfA.StoredVariables["MahalanobisConsistency"].store( float( 2.*MinJ/d.size ) )
    if selfA._toStore("SimulationQuantiles"):
        QuantilesEstimations(selfA, A, Xa, HXa, Hm, HtM)
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
    #
    return 0

# ==============================================================================
def mlef(selfA, Xb, Y, U, HO, EM, CM, R, B, Q,
    VariantM="MLEF13", BnotT=False, _epsilon=1.e-3, _e=1.e-7, _jmax=15000,
    Hybrid=None,
    ):
    """
    Maximum Likelihood Ensemble Filter
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Opérateurs
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
        M = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    # Durée d'observation et tailles
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
        __p = numpy.cumprod(Y.shape())[-1]
    else:
        duration = 2
        __p = numpy.array(Y).size
    #
    # Précalcul des inversions de B et R
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
    RI = R.getI()
    #
    __n = Xb.size
    __m = selfA._parameters["NumberOfMembers"]
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    previousJMinimum = numpy.finfo(float).max
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        Xn = EnsembleOfBackgroundPerturbations( Xb, None, __m )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            if hasattr(B,"asfullmatrix"):
                selfA.StoredVariables["APosterioriCovariance"].store( B.asfullmatrix(__n) )
            else:
                selfA.StoredVariables["APosterioriCovariance"].store( B )
        selfA._setInternalState("seed", numpy.random.get_state())
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
    #
    for step in range(duration-1):
        numpy.random.set_state(selfA._getInternalState("seed"))
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnBackgroundAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast + Q and observation of forecast
            EMX = M( [(Xn[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
            Xn_predicted = EnsemblePerturbationWithGivenCovariance( EMX, Q )
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm @ Un
        elif selfA._parameters["EstimationOf"] == "Parameters": # Observation of forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = EMX = Xn
        #
        #--------------------------
        if VariantM == "MLEF13":
            Xfm = numpy.ravel(Xn_predicted.mean(axis=1, dtype=mfp).astype('float'))
            EaX = EnsembleOfAnomalies( Xn_predicted, Xfm, 1./math.sqrt(__m-1) )
            Ua  = numpy.identity(__m)
            __j = 0
            Deltaw = 1
            if not BnotT:
                Ta  = numpy.identity(__m)
            vw  = numpy.zeros(__m)
            while numpy.linalg.norm(Deltaw) >= _e and __j <= _jmax:
                vx1 = (Xfm + EaX @ vw).reshape((__n,1))
                #
                if BnotT:
                    E1 = vx1 + _epsilon * EaX
                else:
                    E1 = vx1 + math.sqrt(__m-1) * EaX @ Ta
                #
                HE2 = H( [(E1[:,i,numpy.newaxis], Un) for i in range(__m)],
                    argsAsSerie = True,
                    returnSerieAsArrayMatrix = True )
                vy2 = HE2.mean(axis=1, dtype=mfp).astype('float').reshape((__p,1))
                #
                if BnotT:
                    EaY = (HE2 - vy2) / _epsilon
                else:
                    EaY = ( (HE2 - vy2) @ numpy.linalg.inv(Ta) ) / math.sqrt(__m-1)
                #
                GradJ = numpy.ravel(vw[:,None] - EaY.transpose() @ (RI * ( Ynpu - vy2 )))
                mH = numpy.identity(__m) + EaY.transpose() @ (RI * EaY).reshape((-1,__m))
                Deltaw = - numpy.linalg.solve(mH,GradJ)
                #
                vw = vw + Deltaw
                #
                if not BnotT:
                    Ta = numpy.real(scipy.linalg.sqrtm(numpy.linalg.inv( mH )))
                #
                __j = __j + 1
            #
            if BnotT:
                Ta = numpy.real(scipy.linalg.sqrtm(numpy.linalg.inv( mH )))
            #
            Xn = vx1 + math.sqrt(__m-1) * EaX @ Ta @ Ua
        #--------------------------
        else:
            raise ValueError("VariantM has to be chosen in the authorized methods list.")
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnAnalysisAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        if Hybrid == "E3DVAR":
            betaf = selfA._parameters["HybridCovarianceEquilibrium"]
            Xn = Apply3DVarRecentringOnEnsemble(Xn, EMX, Ynpu, HO, R, B, betaf)
        #
        Xa = EnsembleMean( Xn )
        #--------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("seed", numpy.random.get_state())
        #--------------------------
        #
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("APosterioriCovariance") \
            or selfA._toStore("InnovationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            _HXa = numpy.ravel( H((Xa, Un)) ).reshape((-1,1))
            _Innovation = Ynpu - _HXa
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( _HXa )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( EMX )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( EnsembleErrorCovariance(EMX) )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( EMX - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( - HE2 + Ynpu )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HE2 )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T * (BI * (Xa - Xb)) )
            Jo  = float( 0.5 * _Innovation.T * (RI * _Innovation) )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( EnsembleErrorCovariance(Xn) )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = selfA.StoredVariables["APosterioriCovariance"][-1]
        # ---> Pour les smoothers
        if selfA._toStore("CurrentEnsembleState"):
            selfA.StoredVariables["CurrentEnsembleState"].store( Xn )
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def mmqr(
        func     = None,
        x0       = None,
        fprime   = None,
        bounds   = None,
        quantile = 0.5,
        maxfun   = 15000,
        toler    = 1.e-06,
        y        = None,
        ):
    """
    Implémentation informatique de l'algorithme MMQR, basée sur la publication :
    David R. Hunter, Kenneth Lange, "Quantile Regression via an MM Algorithm",
    Journal of Computational and Graphical Statistics, 9, 1, pp.60-77, 2000.
    """
    #
    # Recuperation des donnees et informations initiales
    # --------------------------------------------------
    variables = numpy.ravel( x0 )
    mesures   = numpy.ravel( y )
    increment = sys.float_info[0]
    p         = variables.size
    n         = mesures.size
    quantile  = float(quantile)
    #
    # Calcul des parametres du MM
    # ---------------------------
    tn      = float(toler) / n
    e0      = -tn / math.log(tn)
    epsilon = (e0-tn)/(1+math.log(e0))
    #
    # Calculs d'initialisation
    # ------------------------
    residus  = mesures - numpy.ravel( func( variables ) )
    poids    = 1./(epsilon+numpy.abs(residus))
    veps     = 1. - 2. * quantile - residus * poids
    lastsurrogate = -numpy.sum(residus*veps) - (1.-2.*quantile)*numpy.sum(residus)
    iteration = 0
    #
    # Recherche iterative
    # -------------------
    while (increment > toler) and (iteration < maxfun) :
        iteration += 1
        #
        Derivees  = numpy.array(fprime(variables))
        Derivees  = Derivees.reshape(n,p) # ADAO & check shape
        DeriveesT = Derivees.transpose()
        M         =   numpy.dot( DeriveesT , (numpy.array(numpy.matrix(p*[poids,]).T)*Derivees) )
        SM        =   numpy.transpose(numpy.dot( DeriveesT , veps ))
        step      = - numpy.linalg.lstsq( M, SM, rcond=-1 )[0]
        #
        variables = variables + step
        if bounds is not None:
            # Attention : boucle infinie à éviter si un intervalle est trop petit
            while( (variables < numpy.ravel(numpy.asmatrix(bounds)[:,0])).any() or (variables > numpy.ravel(numpy.asmatrix(bounds)[:,1])).any() ):
                step      = step/2.
                variables = variables - step
        residus   = mesures - numpy.ravel( func(variables) )
        surrogate = numpy.sum(residus**2 * poids) + (4.*quantile-2.) * numpy.sum(residus)
        #
        while ( (surrogate > lastsurrogate) and ( max(list(numpy.abs(step))) > 1.e-16 ) ) :
            step      = step/2.
            variables = variables - step
            residus   = mesures - numpy.ravel( func(variables) )
            surrogate = numpy.sum(residus**2 * poids) + (4.*quantile-2.) * numpy.sum(residus)
        #
        increment     = lastsurrogate-surrogate
        poids         = 1./(epsilon+numpy.abs(residus))
        veps          = 1. - 2. * quantile - residus * poids
        lastsurrogate = -numpy.sum(residus * veps) - (1.-2.*quantile)*numpy.sum(residus)
    #
    # Mesure d'écart
    # --------------
    Ecart = quantile * numpy.sum(residus) - numpy.sum( residus[residus<0] )
    #
    return variables, Ecart, [n,p,iteration,increment,0]

# ==============================================================================
def multi3dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, oneCycle):
    """
    3DVAR multi-pas et multi-méthodes
    """
    #
    # Initialisation
    # --------------
    if selfA._parameters["EstimationOf"] == "State":
        M = EM["Direct"].appliedControledFormTo
        if CM is not None and "Tangent" in CM and U is not None:
            Cm = CM["Tangent"].asMatrix(Xb)
        else:
            Cm = None
        #
        if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
            Xn = numpy.ravel(Xb).reshape((-1,1))
            selfA.StoredVariables["Analysis"].store( Xn )
            if selfA._toStore("APosterioriCovariance"):
                if hasattr(B,"asfullmatrix"):
                    selfA.StoredVariables["APosterioriCovariance"].store( B.asfullmatrix(Xn.size) )
                else:
                    selfA.StoredVariables["APosterioriCovariance"].store( B )
            if selfA._toStore("ForecastState"):
                selfA.StoredVariables["ForecastState"].store( Xn )
        elif selfA._parameters["nextStep"]:
            Xn = selfA._getInternalState("Xn")
    else:
        Xn = numpy.ravel(Xb).reshape((-1,1))
    #
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
    else:
        duration = 2
    #
    # Multi-pas
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((-1,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((-1,1))
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast
            Xn_predicted = M( (Xn, Un) )
            if selfA._toStore("ForecastState"):
                selfA.StoredVariables["ForecastState"].store( Xn_predicted )
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm @ Un
        elif selfA._parameters["EstimationOf"] == "Parameters": # No forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = Xn
        Xn_predicted = numpy.ravel(Xn_predicted).reshape((-1,1))
        #
        oneCycle(selfA, Xn_predicted, Ynpu, None, HO, None, None, R, B, None)
        #
        Xn = selfA.StoredVariables["Analysis"][-1]
        #--------------------------
        selfA._setInternalState("Xn", Xn)
    #
    return 0

# ==============================================================================
def psas3dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    3DVAR PSAS
    """
    #
    # Initialisations
    # ---------------
    Hm = HO["Direct"].appliedTo
    #
    if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
        HXb = numpy.asarray(Hm( Xb, HO["AppliedInX"]["HXb"] ))
    else:
        HXb = numpy.asarray(Hm( Xb ))
    HXb = numpy.ravel( HXb ).reshape((-1,1))
    if Y.size != HXb.size:
        raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
    if max(Y.shape) != max(HXb.shape):
        raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
    #
    if selfA._toStore("JacobianMatrixAtBackground"):
        HtMb = HO["Tangent"].asMatrix(ValueForMethodForm = Xb)
        HtMb = HtMb.reshape(Y.size,Xb.size) # ADAO & check shape
        selfA.StoredVariables["JacobianMatrixAtBackground"].store( HtMb )
    #
    Ht = HO["Tangent"].asMatrix(Xb)
    BHT = B * Ht.T
    HBHTpR = R + Ht * BHT
    Innovation = Y - HXb
    #
    Xini = numpy.zeros(Y.size)
    #
    # Définition de la fonction-coût
    # ------------------------------
    def CostFunction(w):
        _W = numpy.asarray(w).reshape((-1,1))
        if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CurrentState") or \
            selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentState"].store( Xb + BHT @ _W )
        if selfA._toStore("SimulatedObservationAtCurrentState") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( Hm( Xb + BHT @ _W ) )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( Innovation )
        #
        Jb  = float( 0.5 * _W.T @ (HBHTpR @ _W) )
        Jo  = float( - _W.T @ Innovation )
        J   = Jb + Jo
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        if selfA._toStore("IndexOfOptimum") or \
            selfA._toStore("CurrentOptimum") or \
            selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        if selfA._toStore("IndexOfOptimum"):
            selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
        if selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["CurrentState"][IndexMin] )
        if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
        if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
        if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
        if selfA._toStore("CostFunctionJAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        return J
    #
    def GradientOfCostFunction(w):
        _W = numpy.asarray(w).reshape((-1,1))
        GradJb  = HBHTpR @ _W
        GradJo  = - Innovation
        GradJ   = numpy.ravel( GradJb ) + numpy.ravel( GradJo )
        return GradJ
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
    #
    if selfA._parameters["Minimizer"] == "LBFGSB":
        if "0.19" <= scipy.version.version <= "1.1.0":
            import lbfgsbhlt as optimiseur
        else:
            import scipy.optimize as optimiseur
        Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxfun      = selfA._parameters["MaximumNumberOfSteps"]-1,
            factr       = selfA._parameters["CostDecrementTolerance"]*1.e14,
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            iprint      = selfA._parameters["optiprint"],
            )
        nfeval = Informations['funcalls']
        rc     = Informations['warnflag']
    elif selfA._parameters["Minimizer"] == "TNC":
        Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxfun      = selfA._parameters["MaximumNumberOfSteps"],
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            ftol        = selfA._parameters["CostDecrementTolerance"],
            messages    = selfA._parameters["optmessages"],
            )
    elif selfA._parameters["Minimizer"] == "CG":
        Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    elif selfA._parameters["Minimizer"] == "NCG":
        Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            avextol     = selfA._parameters["CostDecrementTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    elif selfA._parameters["Minimizer"] == "BFGS":
        Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    else:
        raise ValueError("Error in Minimizer name: %s"%selfA._parameters["Minimizer"])
    #
    IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
    MinJ     = selfA.StoredVariables["CostFunctionJ"][IndexMin]
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    # ----------------------------------------------------------------
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
    else:
        Minimum = Xb + BHT @ Minimum.reshape((-1,1))
    #
    Xa = Minimum
    #--------------------------
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    if selfA._toStore("OMA") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm( Xa )
    #
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("JacobianMatrixAtOptimum") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HtM = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
        HtM = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HaM = HO["Adjoint"].asMatrix(ValueForMethodForm = Xa)
        HaM = HaM.reshape(Xa.size,Y.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles"):
        BI = B.getI()
        RI = R.getI()
        A = HessienneEstimation(Xa.size, HaM, HtM, BI, RI)
    if selfA._toStore("APosterioriCovariance"):
        selfA.StoredVariables["APosterioriCovariance"].store( A )
    if selfA._toStore("JacobianMatrixAtOptimum"):
        selfA.StoredVariables["JacobianMatrixAtOptimum"].store( HtM )
    if selfA._toStore("KalmanGainAtOptimum"):
        if   (Y.size <= Xb.size): KG  = B * HaM * (R + numpy.dot(HtM, B * HaM)).I
        elif (Y.size >  Xb.size): KG = (BI + numpy.dot(HaM, RI * HtM)).I * HaM * RI
        selfA.StoredVariables["KalmanGainAtOptimum"].store( KG )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("Innovation") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("MahalanobisConsistency") or \
        selfA._toStore("OMB"):
        d  = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( d )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( d )
    if selfA._toStore("SigmaObs2"):
        TraceR = R.trace(Y.size)
        selfA.StoredVariables["SigmaObs2"].store( float( (d.T @ (numpy.ravel(Y)-numpy.ravel(HXa))) ) / TraceR )
    if selfA._toStore("MahalanobisConsistency"):
        selfA.StoredVariables["MahalanobisConsistency"].store( float( 2.*MinJ/d.size ) )
    if selfA._toStore("SimulationQuantiles"):
        QuantilesEstimations(selfA, A, Xa, HXa, Hm, HtM)
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
    #
    return 0

# ==============================================================================
def senkf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q,
    VariantM="KalmanFilterFormula16",
    Hybrid=None,
    ):
    """
    Stochastic EnKF
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Opérateurs
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
        M = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    # Durée d'observation et tailles
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
        __p = numpy.cumprod(Y.shape())[-1]
    else:
        duration = 2
        __p = numpy.array(Y).size
    #
    # Précalcul des inversions de B et R
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
        RI = R.getI()
    #
    __n = Xb.size
    __m = selfA._parameters["NumberOfMembers"]
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    previousJMinimum = numpy.finfo(float).max
    #
    if hasattr(R,"asfullmatrix"): Rn = R.asfullmatrix(__p)
    else:                         Rn = R
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        if hasattr(B,"asfullmatrix"): Pn = B.asfullmatrix(__n)
        else:                         Pn = B
        Xn = EnsembleOfBackgroundPerturbations( Xb, Pn, __m )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        selfA._setInternalState("seed", numpy.random.get_state())
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
    #
    for step in range(duration-1):
        numpy.random.set_state(selfA._getInternalState("seed"))
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnBackgroundAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast + Q and observation of forecast
            EMX = M( [(Xn[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
            Xn_predicted = EnsemblePerturbationWithGivenCovariance( EMX, Q )
            HX_predicted = H( [(Xn_predicted[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm @ Un
        elif selfA._parameters["EstimationOf"] == "Parameters": # Observation of forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = EMX = Xn
            HX_predicted = H( [(Xn_predicted[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
        #
        # Mean of forecast and observation of forecast
        Xfm  = EnsembleMean( Xn_predicted )
        Hfm  = EnsembleMean( HX_predicted )
        #
        #--------------------------
        if VariantM == "KalmanFilterFormula05":
            PfHT, HPfHT = 0., 0.
            for i in range(__m):
                Exfi = Xn_predicted[:,i].reshape((__n,1)) - Xfm
                Eyfi = HX_predicted[:,i].reshape((__p,1)) - Hfm
                PfHT  += Exfi * Eyfi.T
                HPfHT += Eyfi * Eyfi.T
            PfHT  = (1./(__m-1)) * PfHT
            HPfHT = (1./(__m-1)) * HPfHT
            Kn     = PfHT * ( R + HPfHT ).I
            del PfHT, HPfHT
            #
            for i in range(__m):
                ri = numpy.random.multivariate_normal(numpy.zeros(__p), Rn)
                Xn[:,i] = numpy.ravel(Xn_predicted[:,i]) + Kn @ (numpy.ravel(Ynpu) + ri - HX_predicted[:,i])
        #--------------------------
        elif VariantM == "KalmanFilterFormula16":
            EpY   = EnsembleOfCenteredPerturbations(Ynpu, Rn, __m)
            EpYm  = EpY.mean(axis=1, dtype=mfp).astype('float').reshape((__p,1))
            #
            EaX   = EnsembleOfAnomalies( Xn_predicted ) / math.sqrt(__m-1)
            EaY = (HX_predicted - Hfm - EpY + EpYm) / math.sqrt(__m-1)
            #
            Kn = EaX @ EaY.T @ numpy.linalg.inv( EaY @ EaY.T)
            #
            for i in range(__m):
                Xn[:,i] = numpy.ravel(Xn_predicted[:,i]) + Kn @ (numpy.ravel(EpY[:,i]) - HX_predicted[:,i])
        #--------------------------
        else:
            raise ValueError("VariantM has to be chosen in the authorized methods list.")
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnAnalysisAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        if Hybrid == "E3DVAR":
            betaf = selfA._parameters["HybridCovarianceEquilibrium"]
            Xn = Apply3DVarRecentringOnEnsemble(Xn, EMX, Ynpu, HO, R, B, betaf)
        #
        Xa = EnsembleMean( Xn )
        #--------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("seed", numpy.random.get_state())
        #--------------------------
        #
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("APosterioriCovariance") \
            or selfA._toStore("InnovationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            _HXa = numpy.ravel( H((Xa, Un)) ).reshape((-1,1))
            _Innovation = Ynpu - _HXa
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( _HXa )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( EMX )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( EnsembleErrorCovariance(EMX) )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( EMX - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( - HX_predicted + Ynpu )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HX_predicted )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T * (BI * (Xa - Xb)) )
            Jo  = float( 0.5 * _Innovation.T * (RI * _Innovation) )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( EnsembleErrorCovariance(Xn) )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = selfA.StoredVariables["APosterioriCovariance"][-1]
        # ---> Pour les smoothers
        if selfA._toStore("CurrentEnsembleState"):
            selfA.StoredVariables["CurrentEnsembleState"].store( Xn )
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def std3dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    3DVAR
    """
    #
    # Initialisations
    # ---------------
    Hm = HO["Direct"].appliedTo
    Ha = HO["Adjoint"].appliedInXTo
    #
    if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
        HXb = numpy.asarray(Hm( Xb, HO["AppliedInX"]["HXb"] ))
    else:
        HXb = numpy.asarray(Hm( Xb ))
    HXb = HXb.reshape((-1,1))
    if Y.size != HXb.size:
        raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
    if max(Y.shape) != max(HXb.shape):
        raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
    #
    if selfA._toStore("JacobianMatrixAtBackground"):
        HtMb = HO["Tangent"].asMatrix(ValueForMethodForm = Xb)
        HtMb = HtMb.reshape(Y.size,Xb.size) # ADAO & check shape
        selfA.StoredVariables["JacobianMatrixAtBackground"].store( HtMb )
    #
    BI = B.getI()
    RI = R.getI()
    #
    Xini = selfA._parameters["InitializationPoint"]
    #
    # Définition de la fonction-coût
    # ------------------------------
    def CostFunction(x):
        _X  = numpy.asarray(x).reshape((-1,1))
        if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CurrentState") or \
            selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentState"].store( _X )
        _HX = numpy.asarray(Hm( _X )).reshape((-1,1))
        _Innovation = Y - _HX
        if selfA._toStore("SimulatedObservationAtCurrentState") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        #
        Jb  = float( 0.5 * (_X - Xb).T * (BI * (_X - Xb)) )
        Jo  = float( 0.5 * _Innovation.T * (RI * _Innovation) )
        J   = Jb + Jo
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        if selfA._toStore("IndexOfOptimum") or \
            selfA._toStore("CurrentOptimum") or \
            selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        if selfA._toStore("IndexOfOptimum"):
            selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
        if selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["CurrentState"][IndexMin] )
        if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
        if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
        if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
        if selfA._toStore("CostFunctionJAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        return J
    #
    def GradientOfCostFunction(x):
        _X      = numpy.asarray(x).reshape((-1,1))
        _HX     = numpy.asarray(Hm( _X )).reshape((-1,1))
        GradJb  = BI * (_X - Xb)
        GradJo  = - Ha( (_X, RI * (Y - _HX)) )
        GradJ   = numpy.ravel( GradJb ) + numpy.ravel( GradJo )
        return GradJ
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
    #
    if selfA._parameters["Minimizer"] == "LBFGSB":
        if "0.19" <= scipy.version.version <= "1.1.0":
            import lbfgsbhlt as optimiseur
        else:
            import scipy.optimize as optimiseur
        Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfSteps"]-1,
            factr       = selfA._parameters["CostDecrementTolerance"]*1.e14,
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            iprint      = selfA._parameters["optiprint"],
            )
        nfeval = Informations['funcalls']
        rc     = Informations['warnflag']
    elif selfA._parameters["Minimizer"] == "TNC":
        Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfSteps"],
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            ftol        = selfA._parameters["CostDecrementTolerance"],
            messages    = selfA._parameters["optmessages"],
            )
    elif selfA._parameters["Minimizer"] == "CG":
        Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    elif selfA._parameters["Minimizer"] == "NCG":
        Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            avextol     = selfA._parameters["CostDecrementTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    elif selfA._parameters["Minimizer"] == "BFGS":
        Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    else:
        raise ValueError("Error in Minimizer name: %s"%selfA._parameters["Minimizer"])
    #
    IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
    MinJ     = selfA.StoredVariables["CostFunctionJ"][IndexMin]
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    # ----------------------------------------------------------------
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
    #
    Xa = Minimum
    #--------------------------
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    if selfA._toStore("OMA") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm( Xa )
    #
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("JacobianMatrixAtOptimum") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HtM = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
        HtM = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HaM = HO["Adjoint"].asMatrix(ValueForMethodForm = Xa)
        HaM = HaM.reshape(Xa.size,Y.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles"):
        A = HessienneEstimation(Xa.size, HaM, HtM, BI, RI)
    if selfA._toStore("APosterioriCovariance"):
        selfA.StoredVariables["APosterioriCovariance"].store( A )
    if selfA._toStore("JacobianMatrixAtOptimum"):
        selfA.StoredVariables["JacobianMatrixAtOptimum"].store( HtM )
    if selfA._toStore("KalmanGainAtOptimum"):
        if   (Y.size <= Xb.size): KG  = B * HaM * (R + numpy.dot(HtM, B * HaM)).I
        elif (Y.size >  Xb.size): KG = (BI + numpy.dot(HaM, RI * HtM)).I * HaM * RI
        selfA.StoredVariables["KalmanGainAtOptimum"].store( KG )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("Innovation") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("MahalanobisConsistency") or \
        selfA._toStore("OMB"):
        d  = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( d )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( d )
    if selfA._toStore("SigmaObs2"):
        TraceR = R.trace(Y.size)
        selfA.StoredVariables["SigmaObs2"].store( float( (d.T @ (numpy.ravel(Y)-numpy.ravel(HXa))) ) / TraceR )
    if selfA._toStore("MahalanobisConsistency"):
        selfA.StoredVariables["MahalanobisConsistency"].store( float( 2.*MinJ/d.size ) )
    if selfA._toStore("SimulationQuantiles"):
        QuantilesEstimations(selfA, A, Xa, HXa, Hm, HtM)
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
    #
    return 0

# ==============================================================================
def std4dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    4DVAR
    """
    #
    # Initialisations
    # ---------------
    #
    # Opérateurs
    Hm = HO["Direct"].appliedControledFormTo
    Mm = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    def Un(_step):
        if U is not None:
            if hasattr(U,"store") and 1<=_step<len(U) :
                _Un = numpy.ravel( U[_step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                _Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                _Un = numpy.ravel( U ).reshape((-1,1))
        else:
            _Un = None
        return _Un
    def CmUn(_xn,_un):
        if Cm is not None and _un is not None: # Attention : si Cm est aussi dans M, doublon !
            _Cm   = Cm.reshape(_xn.size,_un.size) # ADAO & check shape
            _CmUn = (_Cm @ _un).reshape((-1,1))
        else:
            _CmUn = 0.
        return _CmUn
    #
    # Remarque : les observations sont exploitées à partir du pas de temps
    # numéro 1, et sont utilisées dans Yo comme rangées selon ces indices.
    # Donc le pas 0 n'est pas utilisé puisque la première étape commence
    # avec l'observation du pas 1.
    #
    # Nombre de pas identique au nombre de pas d'observations
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
    else:
        duration = 2
    #
    # Précalcul des inversions de B et R
    BI = B.getI()
    RI = R.getI()
    #
    # Point de démarrage de l'optimisation
    Xini = selfA._parameters["InitializationPoint"]
    #
    # Définition de la fonction-coût
    # ------------------------------
    selfA.DirectCalculation = [None,] # Le pas 0 n'est pas observé
    selfA.DirectInnovation  = [None,] # Le pas 0 n'est pas observé
    def CostFunction(x):
        _X  = numpy.asarray(x).reshape((-1,1))
        if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CurrentState") or \
            selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentState"].store( _X )
        Jb  = float( 0.5 * (_X - Xb).T * (BI * (_X - Xb)) )
        selfA.DirectCalculation = [None,]
        selfA.DirectInnovation  = [None,]
        Jo  = 0.
        _Xn = _X
        for step in range(0,duration-1):
            if hasattr(Y,"store"):
                _Ynpu = numpy.ravel( Y[step+1] ).reshape((-1,1))
            else:
                _Ynpu = numpy.ravel( Y ).reshape((-1,1))
            _Un = Un(step)
            #
            # Etape d'évolution
            if selfA._parameters["EstimationOf"] == "State":
                _Xn = Mm( (_Xn, _Un) ).reshape((-1,1)) + CmUn(_Xn, _Un)
            elif selfA._parameters["EstimationOf"] == "Parameters":
                pass
            #
            if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
                _Xn = ApplyBounds( _Xn, ForceNumericBounds(selfA._parameters["Bounds"]) )
            #
            # Etape de différence aux observations
            if selfA._parameters["EstimationOf"] == "State":
                _YmHMX = _Ynpu - numpy.ravel( Hm( (_Xn, None) ) ).reshape((-1,1))
            elif selfA._parameters["EstimationOf"] == "Parameters":
                _YmHMX = _Ynpu - numpy.ravel( Hm( (_Xn, _Un) ) ).reshape((-1,1)) - CmUn(_Xn, _Un)
            #
            # Stockage de l'état
            selfA.DirectCalculation.append( _Xn )
            selfA.DirectInnovation.append( _YmHMX )
            #
            # Ajout dans la fonctionnelle d'observation
            Jo = Jo + 0.5 * float( _YmHMX.T * (RI * _YmHMX) )
        J = Jb + Jo
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        if selfA._toStore("IndexOfOptimum") or \
            selfA._toStore("CurrentOptimum") or \
            selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        if selfA._toStore("IndexOfOptimum"):
            selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
        if selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["CurrentState"][IndexMin] )
        if selfA._toStore("CostFunctionJAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
        if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
        return J
    #
    def GradientOfCostFunction(x):
        _X      = numpy.asarray(x).reshape((-1,1))
        GradJb  = BI * (_X - Xb)
        GradJo  = 0.
        for step in range(duration-1,0,-1):
            # Étape de récupération du dernier stockage de l'évolution
            _Xn = selfA.DirectCalculation.pop()
            # Étape de récupération du dernier stockage de l'innovation
            _YmHMX = selfA.DirectInnovation.pop()
            # Calcul des adjoints
            Ha = HO["Adjoint"].asMatrix(ValueForMethodForm = _Xn)
            Ha = Ha.reshape(_Xn.size,_YmHMX.size) # ADAO & check shape
            Ma = EM["Adjoint"].asMatrix(ValueForMethodForm = _Xn)
            Ma = Ma.reshape(_Xn.size,_Xn.size) # ADAO & check shape
            # Calcul du gradient par état adjoint
            GradJo = GradJo + Ha * (RI * _YmHMX) # Équivaut pour Ha linéaire à : Ha( (_Xn, RI * _YmHMX) )
            GradJo = Ma * GradJo                 # Équivaut pour Ma linéaire à : Ma( (_Xn, GradJo) )
        GradJ = numpy.ravel( GradJb ) - numpy.ravel( GradJo )
        return GradJ
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
    #
    if selfA._parameters["Minimizer"] == "LBFGSB":
        if "0.19" <= scipy.version.version <= "1.1.0":
            import lbfgsbhlt as optimiseur
        else:
            import scipy.optimize as optimiseur
        Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfSteps"]-1,
            factr       = selfA._parameters["CostDecrementTolerance"]*1.e14,
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            iprint      = selfA._parameters["optiprint"],
            )
        nfeval = Informations['funcalls']
        rc     = Informations['warnflag']
    elif selfA._parameters["Minimizer"] == "TNC":
        Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfSteps"],
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            ftol        = selfA._parameters["CostDecrementTolerance"],
            messages    = selfA._parameters["optmessages"],
            )
    elif selfA._parameters["Minimizer"] == "CG":
        Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    elif selfA._parameters["Minimizer"] == "NCG":
        Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            avextol     = selfA._parameters["CostDecrementTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    elif selfA._parameters["Minimizer"] == "BFGS":
        Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    else:
        raise ValueError("Error in Minimizer name: %s"%selfA._parameters["Minimizer"])
    #
    IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
    MinJ     = selfA.StoredVariables["CostFunctionJ"][IndexMin]
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    # ----------------------------------------------------------------
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
    #
    # Obtention de l'analyse
    # ----------------------
    Xa = Minimum
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    #
    return 0

# ==============================================================================
def stdkf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    Standard Kalman Filter
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Opérateurs
    # ----------
    Ht = HO["Tangent"].asMatrix(Xb)
    Ha = HO["Adjoint"].asMatrix(Xb)
    #
    if selfA._parameters["EstimationOf"] == "State":
        Mt = EM["Tangent"].asMatrix(Xb)
        Ma = EM["Adjoint"].asMatrix(Xb)
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    # Durée d'observation et tailles
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
        __p = numpy.cumprod(Y.shape())[-1]
    else:
        duration = 2
        __p = numpy.array(Y).size
    #
    # Précalcul des inversions de B et R
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
        RI = R.getI()
    #
    __n = Xb.size
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        Xn = Xb
        Pn = B
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            if hasattr(B,"asfullmatrix"):
                selfA.StoredVariables["APosterioriCovariance"].store( B.asfullmatrix(__n) )
            else:
                selfA.StoredVariables["APosterioriCovariance"].store( B )
        selfA._setInternalState("seed", numpy.random.get_state())
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
        Pn = selfA._getInternalState("Pn")
    #
    if selfA._parameters["EstimationOf"] == "Parameters":
        XaMin            = Xn
        previousJMinimum = numpy.finfo(float).max
    #
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast + Q and observation of forecast
            Xn_predicted = Mt @ Xn
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm @ Un
            Pn_predicted = Q + Mt * (Pn * Ma)
        elif selfA._parameters["EstimationOf"] == "Parameters": # Observation of forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = Xn
            Pn_predicted = Pn
        #
        if selfA._parameters["EstimationOf"] == "State":
            HX_predicted = Ht @ Xn_predicted
            _Innovation  = Ynpu - HX_predicted
        elif selfA._parameters["EstimationOf"] == "Parameters":
            HX_predicted = Ht @ Xn_predicted
            _Innovation  = Ynpu - HX_predicted
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans H, doublon !
                _Innovation = _Innovation - Cm @ Un
        #
        Kn = Pn_predicted * Ha * numpy.linalg.inv(R + numpy.dot(Ht, Pn_predicted * Ha))
        Xn = Xn_predicted + Kn * _Innovation
        Pn = Pn_predicted - Kn * Ht * Pn_predicted
        #
        Xa = Xn # Pointeurs
        #--------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("Pn", Pn)
        #--------------------------
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( Ht * Xa )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( Xn_predicted )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( Pn_predicted )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( Xn_predicted - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HX_predicted )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T * (BI * (Xa - Xb)) )
            Jo  = float( 0.5 * _Innovation.T * (RI * _Innovation) )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = selfA.StoredVariables["APosterioriCovariance"][-1]
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def uskf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    Unscented Kalman Filter
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    L     = Xb.size
    Alpha = selfA._parameters["Alpha"]
    Beta  = selfA._parameters["Beta"]
    if selfA._parameters["Kappa"] == 0:
        if selfA._parameters["EstimationOf"] == "State":
            Kappa = 0
        elif selfA._parameters["EstimationOf"] == "Parameters":
            Kappa = 3 - L
    else:
        Kappa = selfA._parameters["Kappa"]
    Lambda = float( Alpha**2 ) * ( L + Kappa ) - L
    Gamma  = math.sqrt( L + Lambda )
    #
    Ww = []
    Ww.append( 0. )
    for i in range(2*L):
        Ww.append( 1. / (2.*(L + Lambda)) )
    #
    Wm = numpy.array( Ww )
    Wm[0] = Lambda / (L + Lambda)
    Wc = numpy.array( Ww )
    Wc[0] = Lambda / (L + Lambda) + (1. - Alpha**2 + Beta)
    #
    # Opérateurs
    Hm = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
        Mm = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    # Durée d'observation et tailles
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
        __p = numpy.cumprod(Y.shape())[-1]
    else:
        duration = 2
        __p = numpy.array(Y).size
    #
    # Précalcul des inversions de B et R
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
        RI = R.getI()
    #
    __n = Xb.size
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        Xn = Xb
        if hasattr(B,"asfullmatrix"):
            Pn = B.asfullmatrix(__n)
        else:
            Pn = B
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
        Pn = selfA._getInternalState("Pn")
    #
    if selfA._parameters["EstimationOf"] == "Parameters":
        XaMin            = Xn
        previousJMinimum = numpy.finfo(float).max
    #
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        Pndemi = numpy.real(scipy.linalg.sqrtm(Pn))
        Xnp = numpy.hstack([Xn, Xn+Gamma*Pndemi, Xn-Gamma*Pndemi])
        nbSpts = 2*Xn.size+1
        #
        XEtnnp = []
        for point in range(nbSpts):
            if selfA._parameters["EstimationOf"] == "State":
                XEtnnpi = numpy.asarray( Mm( (Xnp[:,point], Un) ) ).reshape((-1,1))
                if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                    Cm = Cm.reshape(Xn.size,Un.size) # ADAO & check shape
                    XEtnnpi = XEtnnpi + Cm @ Un
            elif selfA._parameters["EstimationOf"] == "Parameters":
                # --- > Par principe, M = Id, Q = 0
                XEtnnpi = Xnp[:,point]
            XEtnnp.append( numpy.ravel(XEtnnpi).reshape((-1,1)) )
        XEtnnp = numpy.concatenate( XEtnnp, axis=1 )
        #
        Xncm = ( XEtnnp * Wm ).sum(axis=1)
        #
        if selfA._parameters["EstimationOf"] == "State":        Pnm = Q
        elif selfA._parameters["EstimationOf"] == "Parameters": Pnm = 0.
        for point in range(nbSpts):
            Pnm += Wc[i] * ((XEtnnp[:,point]-Xncm).reshape((-1,1)) * (XEtnnp[:,point]-Xncm))
        #
        Pnmdemi = numpy.real(scipy.linalg.sqrtm(Pnm))
        #
        Xnnp = numpy.hstack([Xncm.reshape((-1,1)), Xncm.reshape((-1,1))+Gamma*Pnmdemi, Xncm.reshape((-1,1))-Gamma*Pnmdemi])
        #
        Ynnp = []
        for point in range(nbSpts):
            if selfA._parameters["EstimationOf"] == "State":
                Ynnpi = Hm( (Xnnp[:,point], None) )
            elif selfA._parameters["EstimationOf"] == "Parameters":
                Ynnpi = Hm( (Xnnp[:,point], Un) )
            Ynnp.append( numpy.ravel(Ynnpi).reshape((-1,1)) )
        Ynnp = numpy.concatenate( Ynnp, axis=1 )
        #
        Yncm = ( Ynnp * Wm ).sum(axis=1)
        #
        Pyyn = R
        Pxyn = 0.
        for point in range(nbSpts):
            Pyyn += Wc[i] * ((Ynnp[:,point]-Yncm).reshape((-1,1)) * (Ynnp[:,point]-Yncm))
            Pxyn += Wc[i] * ((Xnnp[:,point]-Xncm).reshape((-1,1)) * (Ynnp[:,point]-Yncm))
        #
        _Innovation  = Ynpu - Yncm.reshape((-1,1))
        if selfA._parameters["EstimationOf"] == "Parameters":
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans H, doublon !
                _Innovation = _Innovation - Cm @ Un
        #
        Kn = Pxyn * Pyyn.I
        Xn = Xncm.reshape((-1,1)) + Kn * _Innovation
        Pn = Pnm - Kn * Pyyn * Kn.T
        #
        Xa = Xn # Pointeurs
        #--------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("Pn", Pn)
        #--------------------------
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( Hm((Xa, Un)) )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( Xncm )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( Pnm )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( Xncm - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( Yncm )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T * (BI * (Xa - Xb)) )
            Jo  = float( 0.5 * _Innovation.T * (RI * _Innovation) )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = selfA.StoredVariables["APosterioriCovariance"][-1]
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def van3dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    3DVAR variational analysis with no inversion of B
    """
    #
    # Initialisations
    # ---------------
    Hm = HO["Direct"].appliedTo
    Ha = HO["Adjoint"].appliedInXTo
    #
    BT = B.getT()
    RI = R.getI()
    #
    Xini = numpy.zeros(Xb.size)
    #
    # Définition de la fonction-coût
    # ------------------------------
    def CostFunction(v):
        _V = numpy.asarray(v).reshape((-1,1))
        _X = Xb + (B @ _V).reshape((-1,1))
        if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CurrentState") or \
            selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentState"].store( _X )
        _HX = numpy.asarray(Hm( _X )).reshape((-1,1))
        _Innovation = Y - _HX
        if selfA._toStore("SimulatedObservationAtCurrentState") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        #
        Jb  = float( 0.5 * _V.T * (BT * _V) )
        Jo  = float( 0.5 * _Innovation.T * (RI * _Innovation) )
        J   = Jb + Jo
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        if selfA._toStore("IndexOfOptimum") or \
            selfA._toStore("CurrentOptimum") or \
            selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        if selfA._toStore("IndexOfOptimum"):
            selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
        if selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["CurrentState"][IndexMin] )
        if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
        if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
        if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
        if selfA._toStore("CostFunctionJAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        return J
    #
    def GradientOfCostFunction(v):
        _V = numpy.asarray(v).reshape((-1,1))
        _X = Xb + (B @ _V).reshape((-1,1))
        _HX     = numpy.asarray(Hm( _X )).reshape((-1,1))
        GradJb  = BT * _V
        GradJo  = - Ha( (_X, RI * (Y - _HX)) )
        GradJ   = numpy.ravel( GradJb ) + numpy.ravel( GradJo )
        return GradJ
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
    #
    if selfA._parameters["Minimizer"] == "LBFGSB":
        if "0.19" <= scipy.version.version <= "1.1.0":
            import lbfgsbhlt as optimiseur
        else:
            import scipy.optimize as optimiseur
        Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = RecentredBounds(selfA._parameters["Bounds"], Xb),
            maxfun      = selfA._parameters["MaximumNumberOfSteps"]-1,
            factr       = selfA._parameters["CostDecrementTolerance"]*1.e14,
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            iprint      = selfA._parameters["optiprint"],
            )
        nfeval = Informations['funcalls']
        rc     = Informations['warnflag']
    elif selfA._parameters["Minimizer"] == "TNC":
        Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = RecentredBounds(selfA._parameters["Bounds"], Xb),
            maxfun      = selfA._parameters["MaximumNumberOfSteps"],
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            ftol        = selfA._parameters["CostDecrementTolerance"],
            messages    = selfA._parameters["optmessages"],
            )
    elif selfA._parameters["Minimizer"] == "CG":
        Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    elif selfA._parameters["Minimizer"] == "NCG":
        Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            avextol     = selfA._parameters["CostDecrementTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    elif selfA._parameters["Minimizer"] == "BFGS":
        Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    else:
        raise ValueError("Error in Minimizer name: %s"%selfA._parameters["Minimizer"])
    #
    IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
    MinJ     = selfA.StoredVariables["CostFunctionJ"][IndexMin]
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    # ----------------------------------------------------------------
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
    else:
        Minimum = Xb + B * Minimum.reshape((-1,1)) # Pas @
    #
    Xa = Minimum
    #--------------------------
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    if selfA._toStore("OMA") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm( Xa )
    #
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("JacobianMatrixAtOptimum") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HtM = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
        HtM = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HaM = HO["Adjoint"].asMatrix(ValueForMethodForm = Xa)
        HaM = HaM.reshape(Xa.size,Y.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles"):
        BI = B.getI()
        A = HessienneEstimation(Xa.size, HaM, HtM, BI, RI)
    if selfA._toStore("APosterioriCovariance"):
        selfA.StoredVariables["APosterioriCovariance"].store( A )
    if selfA._toStore("JacobianMatrixAtOptimum"):
        selfA.StoredVariables["JacobianMatrixAtOptimum"].store( HtM )
    if selfA._toStore("KalmanGainAtOptimum"):
        if   (Y.size <= Xb.size): KG  = B * HaM * (R + numpy.dot(HtM, B * HaM)).I
        elif (Y.size >  Xb.size): KG = (BI + numpy.dot(HaM, RI * HtM)).I * HaM * RI
        selfA.StoredVariables["KalmanGainAtOptimum"].store( KG )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("Innovation") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("MahalanobisConsistency") or \
        selfA._toStore("OMB"):
        d  = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( d )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( d )
    if selfA._toStore("SigmaObs2"):
        TraceR = R.trace(Y.size)
        selfA.StoredVariables["SigmaObs2"].store( float( (d.T @ (numpy.ravel(Y)-numpy.ravel(HXa))) ) / TraceR )
    if selfA._toStore("MahalanobisConsistency"):
        selfA.StoredVariables["MahalanobisConsistency"].store( float( 2.*MinJ/d.size ) )
    if selfA._toStore("SimulationQuantiles"):
        QuantilesEstimations(selfA, A, Xa, HXa, Hm, HtM)
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
