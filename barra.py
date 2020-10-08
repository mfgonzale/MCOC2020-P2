import numpy as np

g = 9.81 #kg*m/s^2


class Barra(object):

	"""Constructor para una barra"""
	def __init__(self, ni, nj, R, t, E, ρ, σy):
		super(Barra, self).__init__()
		self.ni = ni
		self.nj = nj
		self.R = R
		self.t = t
		self.E = E
		self.ρ = ρ
		self.σy = σy

	def obtener_conectividad(self):
		return [self.ni, self.nj]

	def calcular_area(self):
		A = np.pi*(self.R**2) - np.pi*((self.R-self.t)**2)
		return A

	def calcular_largo(self, reticulado):
		"""Devuelve el largo de la barra. 
		xi : Arreglo numpy de dimenson (3,) con coordenadas del nodo i
		xj : Arreglo numpy de dimenson (3,) con coordenadas del nodo j
		"""
		xi = reticulado.obtener_coordenada_nodal(self.ni)
		xj = reticulado.obtener_coordenada_nodal(self.nj)
		dij = xi-xj
		return np.sqrt(np.dot(dij,dij))

	def calcular_peso(self, reticulado):
		"""Devuelve el largo de la barra. 
		xi : Arreglo numpy de dimenson (3,) con coordenadas del nodo i
		xj : Arreglo numpy de dimenson (3,) con coordenadas del nodo j
		"""
		L = self.calcular_largo(reticulado)
		A = self.calcular_area()
		return self.ρ * A * L * g











	def obtener_rigidez(self, ret):
		A = self.calcular_area()
		L = self.calcular_largo(ret)

		xi = ret.obtener_coordenada_nodal(self.ni)
		xj = ret.obtener_coordenada_nodal(self.nj)

		cosθ = (xj[0] - xi[0])/L
		sinθ = (xj[1] - xi[1])/L

		Tθ = np.array([ -cosθ, -sinθ, cosθ, sinθ ]).reshape((4,1))

		return self.E * A / L * (Tθ @ Tθ.T )

	def obtener_vector_de_cargas(self, ret):
		W = self.calcular_peso(ret)

		return np.array([0, -W, 0, -W])


	def obtener_fuerza(self, ret):
		ue = np.zeros(4)
		ue[0:2] = ret.obtener_desplazamiento_nodal(self.ni)
		ue[2:] = ret.obtener_desplazamiento_nodal(self.nj)
		
		A = self.calcular_area()
		L = self.calcular_largo(ret)

		xi = ret.obtener_coordenada_nodal(self.ni)
		xj = ret.obtener_coordenada_nodal(self.nj)

		cosθ = (xj[0] - xi[0])/L
		sinθ = (xj[1] - xi[1])/L

		Tθ = np.array([ -cosθ, -sinθ, cosθ, sinθ ]).reshape((4,1))

		return self.E * A / L * (Tθ.T @ ue)





	def chequear_diseño(self, Fu, ret, ϕ=0.9,R=self.R,t=self.t):
		"""Para la fuerza Fu (proveniente de una combinacion de cargas)
		revisar si esta barra cumple las disposiciones de diseño.
		"""
		L = self.calcular_largo(ret)
		A = np.pi*(R**2) - np.pi*((R-t)**2)
		I = (np.pi/4)*(R**4 - (R - t)**4)
		i = np.sqrt(I/A)
		esbeltez = L/i
		if esbeltez<300:
			#print(f'Barra {[self.ni,self.nj]} es muy esbelta')
			return False
		elif Fu>0:
			Pn = min(A*self.σy,(np.pi**2)*self.E*I/(L**2))
			if Pn*ϕ<Fu:
				#print(f'Barra {[self.ni,self.nj]} falla en compresion')
				return False
		elif Fu<0:
			Fn = A*self.σy
			if Fn*ϕ<-Fu:
				#print(f'Barra {[self.ni,self.nj]} falla en traccion')
				return False
		else:
			return True


	def obtener_factor_utilizacion(self, Fu, ϕ=0.9):
		"""Para la fuerza Fu (proveniente de una combinacion de cargas)
		calcular y devolver el factor de utilización
		"""
		A = self.calcular_area()

		if Fu>0:
			Pn = A*self.σy#min(A*self.σy,(np.pi**2)*self.E*I/(self.L**2))
			FU = Fu/(Pn*ϕ)
		elif Fu<0:
			Fn = A*self.σy
			FU = -Fu/(Fn*ϕ)
		else:
			FU = 0.

		return FU


	def rediseñar(self, Fu, ret, ϕ=0.9):
		"""Para la fuerza Fu (proveniente de una combinacion de cargas)
		re-calcular el radio y el espesor de la barra de modo que
		se cumplan las disposiciones de diseño lo más cerca posible
		a FU = 1.0.
		"""
		FU = self.obtener_factor_utilizacion(Fu, ϕ)
		L = self.calcular_largo(ret)
		if FU == 1:
			return None
		if Fu<0:
			Areq = -Fu/(ϕ*self.σy)
			Rmin = int(np.sqrt(Areq/np.pi))
			R = np.linspace(Rmin,Rmin + 50.,51)
			soluciones = [Rmin,Rmin]#R,t
			Amin = Areq + 200.
			for r in R
				t = int((np.sqrt(np.pi*r**2 - Areq) + r*np.sqrt(np.pi))/np.sqrt(np.pi))
				A = np.pi*(r**2) - np.pi*((r-t)**2)
				if self.chequear_diseño(Fu, ret, ϕ,R=r,t=t) and A<Amin:
					soluciones[0] = r
					soluciones[1] = t
					Amin = A
			if not self.chequear_diseño(Fu, ret, ϕ,R=soluciones[0],t=soluciones[1]):
				return None
			else:
				self.R = soluciones[0]
				self.t = soluciones[1]
				return None
		if Fu>=0:
			Areq = Fu/(ϕ*self.σy)
			Rmin = int(np.sqrt(Areq/np.pi))
			R = np.linspace(Rmin,Rmin + 50.,51)
			soluciones = [Rmin,Rmin]#R,t
			Amin = Areq + 200.
			for r in R
				t = int((np.sqrt(np.pi*r**2 - Areq) + r*np.sqrt(np.pi))/np.sqrt(np.pi))
				A = np.pi*(r**2) - np.pi*((r-t)**2)
				if self.chequear_diseño(Fu, ret, ϕ,R=r,t=t) and A<Amin:
					soluciones[0] = r
					soluciones[1] = t
					Amin = A
			if not self.chequear_diseño(Fu, ret, ϕ,R=soluciones[0],t=soluciones[1]):
				return None
			else:
				self.R = soluciones[0]
				self.t = soluciones[1]
				return None
		#self.R = 0.9*self.R   #cambiar y poner logica de diseño
		#self.t = 0.9*self.t   #cambiar y poner logica de diseño
		return None


