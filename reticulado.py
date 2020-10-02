import numpy as np

class Reticulado(object):
    """Define un reticulado"""

    def __init__(self):
        super(Reticulado, self).__init__()

        self.xyz = np.zeros((0,3), dtype=np.double)
        self.Nnodos = 0
        self.barras = []
        self.cargas = {}
        self.restricciones = {}
        self.Ndimensiones = 2
        self.tiene_solucion = False

    def agregar_nodo(self, x, y, z=0):
        #Cambiar Tamaño
        self.xyz.resize((self.Nnodos+1,3))
        self.xyz[self.Nnodos,:] = [x,y,z]
        self.Nnodos +=1
        return

    def agregar_barra(self, barra):
	    self.barras.append(barra)
	    return

    def obtener_coordenada_nodal(self, n):
        if n>= self.Nnodos:
            return
        return self.xyz[n,:]
    def calcular_peso_total(self):
        w=0
        for i in self.barras:
            w += i.calcular_peso(self)
        return w
    def obtener_nodos(self):
        return self.xyz

    def obtener_barras(self):
        return self.barras

    def agregar_restriccion(self, nodo, gdl, valor=0.0):
        if nodo not in self.restricciones:
            self.restricciones[nodo] = [[gdl,valor]]
        else:
            self.restricciones[nodo].append([gdl,valor])

    def agregar_fuerza(self, nodo, gdl, valor):
        if nodo not in self.cargas:
            self.cargas[nodo] = [[gdl,valor]]
        else:
            self.cargas[nodo].append([gdl,valor])

    def ensamblar_sistema(self):

        Ngdl = self.Nnodos * self.Ndimensiones
        self.K= np.zeros((Ngdl,Ngdl), dtype=np.double)
        self.f= np.zeros((Ngdl), dtype=np.double)
        self.u= np.zeros((Ngdl), dtype=np.double)

        for b in self.barras:
            ke= b.obtener_rigidez(self)
            fe= b.obtener_vector_de_cargas(self)
            ni,nj = b.obtener_conectividad()
            d= [2*ni,2*ni+1,2*nj,2*nj+1]
            ReaccionesPorBarra = 2*(self.Ndimensiones)
            #MRG
            for i in range(ReaccionesPorBarra):
                p=d[i]
                for j in range(ReaccionesPorBarra):
                    q = d[j]
                    self.K[p,q] += ke[i,j]
                self.f[p] += fe[j]

    def obtener_desplazamiento_nodal(self,n):
	dofs = [2*n, 2*n+1]
	return self.u[dofs]

    def recuperar_fuerzas(self):
        fuerzas = np.zeros((len(self.barras)), dtype=np.double)
        for i,b in enumerate(self.barras):
		fuerzas[i] = b.obtener_fuerza(self)
        return fuerzas

    def resolver_sistema(self):

        uc = []
        uf = [] 
        for i in self.restricciones:
            if i[1] == 0:
                uc.append(i[1])
            else:
                uf.append(i[1])
        
        for b in self.barras:
            k= b.obtener_rigidez(self)

    
        kff = k[np.ix_(uf, uf)]
        kfc = k[np.ix_(uf, uc)]
        kcf = kfc.T
        kcc = k[np.ix_(uc, uc)]

        ff = kff@uf
        fc = kcc@uc

        uf = solve(kff, ff - kfc@uc)

        self.rc = kcf@uf + kcc@uc - fc

        u =[uc,uf]
        return u
    
    
    def _str_(self):
        s = "Reticulado: \n"
        s += "Nodos: \n"
        for n in range(self.Nnodos):
            s += f"{n} : ({self.xyz[n,0]}, {self.xyz[n,1]}, {self.xyz[n,2]}, {self.xyz[n,3]}, {self.xyz[n,4]})\n"
        s += "\n\n"

        s += "Barras: \n"
        for i, b in enumerate(self.barras):
            n = b.obtener_conectividad()
            s += f"{i} : [ {n[0]} {n[1]} ] \n"
        s += "\n\n"

        s += "Restricciones: \n"
        for d in self.restricciones:
        	s += f"{d} : {self.restricciones[d]} \n"
        s += "\n\n"
    
        s += "Cargas: \n"
        for d in self.cargas:
        	s += f"{d} : {self.cargas[d]} \n"
        s += "\n\n"
            
            
        if self.tiene_solucion:
            s += "desplazamientos:\n"
            if self.Ndimensiones == 2:
                uvw = self.u.reshape((-1,2))
                for n in range(self.Nnodos):
                    s += f"  {n} : ( {uvw[n,0]}, {uvw[n,1]}) \n "
        s += "\n\n"

        if self.tiene_solucion:
            f = self.recuperar_fuerzas()
            s += "fuerzas:\n"
            for b in range(len(self.barras)):
                s += f"  {b} : {f[b]}\n"
        s += "\n"
    
        
        return s

