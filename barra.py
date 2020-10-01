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
		return [self.ni,self.nj]

	def calcular_area(self):
		try:
			return self.A
		except:
			self.A = np.pi*(2*self.R*self.t - self.t**2)
			return self.A


	def calcular_largo(self, reticulado):
		"""Devuelve el largo de la barra. 
		xi : Arreglo numpy de dimenson (3,) con coordenadas del nodo i
		xj : Arreglo numpy de dimenson (3,) con coordenadas del nodo j
		"""
		try:
			return self.L
		except:
			xi = reticulado.xyz[self.ni]
			xj = reticulado.xyz[self.nj]
			self.L = np.sqrt( (xi[0]-xj[0])**2 + (xi[1]-xj[1])**2 + (xi[2]-xj[2])**2 )
			return self.L

	def calcular_peso(self, reticulado):
		"""Devuelve el peso de la barra. 
		xi : Arreglo numpy de dimenson (3,) con coordenadas del nodo i
		xj : Arreglo numpy de dimenson (3,) con coordenadas del nodo j
		"""
		try:
			return self.M
		except:
			try:
				A = self.A
			except:
				A = self.calcular_area()
			try:
				L = self.L
			except:
				L = self.calcular_largo(reticulado)
			
			self.M = A*L*g*self.ρ
			return self.M

	def obtener_rigidez(self, ret):
		"""Devuelve la rigidez ke del elemento. Arreglo numpy de (4x4)
		ret: instancia de objeto tipo reticulado
		"""


		L = self.calcular_largo(ret)
		A = self.calcular_area()
		k = self.E * A/L
		
		[xi,yi,zi] = ret.xyz[self.ni]
		[xj,yj,zj] = ret.xyz[self.nj]
		
		self.the = np.arccos((xj-xi)/L)
		
		self.Tthe = np.matrix([-np.cos(the),-np.sin(the),np.cos(the),np.sin(the)])
		
		ke = (Tthe.T @ Tthe)*k
		
		return np.array(ke)
		
	def obtener_vector_de_cargas(self, ret):
		"""Devuelve el vector de cargas nodales fe del elemento. Vector numpy de (4x1)
		ret: instancia de objeto tipo reticulado
		"""
		W = self.calcular_peso(ret)
		ni,nj=self.ni,self.nj
		
		fe = np.zeros(4)
		
		fe[1]-=W/2.
		fe[3]-=W/2.
		
		if ni in ret.cargas:
			for f in ret.cargas[ni]:
				fe[f[0]] += f[1]
		if nj in ret.cargas:
			for f in ret.cargas[nj]:
				fe[f[0]+2] += f[1]
        
		return np.array(np.matrix(fe).T)


	def obtener_fuerza(self, ret):
		"""Devuelve la fuerza se que debe resistir la barra. Un escalar tipo double. 
		ret: instancia de objeto tipo reticulado
		"""
		Thte = 5
		se = A*E/L * Tthe.T * ue
		
		return se






