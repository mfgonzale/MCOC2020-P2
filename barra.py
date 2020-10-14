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

		cosθx = (xj[0] - xi[0])/L
		cosθy = (xj[1] - xi[1])/L
		cosθz = (xj[2] - xi[2])/L

		Tθ = np.array([ -cosθx,-cosθy,-cosθz,cosθx,cosθy,cosθz]).reshape((6,1))

		return self.E * A / L * (Tθ @ Tθ.T )

	def obtener_vector_de_cargas(self, ret):
		W = self.calcular_peso(ret)

		return np.array([0, 0, -W, 0, 0, -W])


	def obtener_fuerza(self, ret):
		ue = np.zeros(6)
		ue[0:3] = ret.obtener_desplazamiento_nodal(self.ni)
		ue[3:] = ret.obtener_desplazamiento_nodal(self.nj)
		
		A = self.calcular_area()
		L = self.calcular_largo(ret)

		xi = ret.obtener_coordenada_nodal(self.ni)
		xj = ret.obtener_coordenada_nodal(self.nj)

		cosθx = (xj[0] - xi[0])/L
		cosθy = (xj[1] - xi[1])/L
		cosθz = (xj[2] - xi[2])/L

		Tθ = np.array([ -cosθx,-cosθy,-cosθz,cosθx,cosθy,cosθz]).reshape((6,1))

		return self.E * A / L * (Tθ.T @ ue)





	def chequear_diseño(self, Fu, ret, ϕ=0.9,R=None,t=None):
		"""Para la fuerza Fu (proveniente de una combinacion de cargas)
		revisar si esta barra cumple las disposiciones de diseño.
		"""
		if R==0 or t==0:
			return False
		if R==None or t==None:
			R = self.R
			t = self.t
		if t>R:
			return False
		L = self.calcular_largo(ret)
		A = np.pi*(R**2) - np.pi*((R-t)**2)
		I = (np.pi/4)*(R**4 - (R - t)**4)
		i = np.sqrt(I/A)
		esbeltez = L/i
		if esbeltez<300.:
			#print(f'Barra {[self.ni,self.nj]} es muy esbelta')
			#print(f'{L},{R},{t}')
			#print(esbeltez)
			return False
		elif Fu>0:
			Pn = min(A*self.σy,(np.pi**2)*self.E*I/(L**2))
			if Pn*ϕ<Fu:
				#print(f'Barra {[self.ni,self.nj]} falla en compresion')
				return False
			else:
				return True
		elif Fu<0:
			Fn = A*self.σy
			if Fn*ϕ<-Fu:
				#print(f'Barra {[self.ni,self.nj]} falla en traccion')
				return False
			else:
				return True
		else:
			print(True)
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
		if FU == 1 and self.chequear_diseño(Fu, ret, ϕ):
			return None
		if Fu<0:
			Areq = -Fu/(ϕ*self.σy)
			Rmin = int(np.sqrt(Areq/np.pi)*1000.)/1000.
			if Rmin==0.0:
				Rmin = 0.001
			R = np.linspace(Rmin,Rmin + .500,501)
			soluciones = [Rmin,Rmin]#R,t
			Amin = Areq+1.
			for r in R:
				if (np.pi*r**2 - Areq)<0. or r==0:
					continue
				tmin = - (np.sqrt(np.pi*r**2 - Areq) - r*np.sqrt(np.pi))/np.sqrt(np.pi)
				#print(f'r= {r}, tmin = {tmin}')
				#print(tmin)
				#print(np.linspace(0.,r,int(r*1000.)+1))
				for t in np.linspace(0.,r,int(r*1000.)+1):
					if t==0 or t<tmin:
						continue
					A = np.pi*(r**2) - np.pi*((r-t)**2)
					#print(A)
					if self.chequear_diseño(Fu, ret, ϕ,R=r,t=t) and A<Amin:
						#print(t)
						soluciones[0] = r
						soluciones[1] = t
						Amin = A
				#print(f"A = {A},Amin={Amin}")
			if not self.chequear_diseño(Fu, ret, ϕ,R=soluciones[0],t=soluciones[1]):
				return None
			else:
				self.R = soluciones[0]
				self.t = soluciones[1]
				return None
		if Fu>=0:
			Areq = Fu/(ϕ*self.σy)
			Rmin = int(np.sqrt(Areq/np.pi)*1000.)/1000.
			if Rmin==0.0:
				Rmin = 0.001
			R = np.linspace(Rmin,Rmin + .500,501)
			soluciones = [Rmin,Rmin]#R,t
			Amin = Areq+1.
			for r in R:
				if (np.pi*r**2 - Areq)<0. or r==0:
					continue
				tmin = - (np.sqrt(np.pi*r**2 - Areq) - r*np.sqrt(np.pi))/np.sqrt(np.pi)
				#print(f'r= {r}, tmin = {tmin}')
				#print(tmin)
				#print(np.linspace(0.,r,int(r*1000.)+1))
				for t in np.linspace(0.,r,int(r*1000.)+1):
					if t==0 or t<tmin:
						continue
					A = np.pi*(r**2) - np.pi*((r-t)**2)
					#print(A)
					if self.chequear_diseño(Fu, ret, ϕ,R=r,t=t) and A<Amin:
						#print(t)
						soluciones[0] = r
						soluciones[1] = t
						Amin = A
				#print(f"A = {A},Amin={Amin}")
			if not self.chequear_diseño(Fu, ret, ϕ,R=soluciones[0],t=soluciones[1]):
				return None
			else:
				self.R = soluciones[0]
				self.t = soluciones[1]
				return None
		#self.R = 0.9*self.R   #cambiar y poner logica de diseño
		#self.t = 0.9*self.t   #cambiar y poner logica de diseño
		return None


