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









