from numpy import zeros, matrix, array, matmul, cross, add
from numpy.linalg import inv, norm
from PyNite.LoadCombo import LoadCombo

#%%
class Plate3D():

    def __init__(self, Name, i_node, j_node, m_node, n_node, t, E, nu,
                 LoadCombos={'Combo 1':LoadCombo('Combo 1', factors={'Case 1':1.0})}):
        """
        A rectangular plate element

        Parameters
        ----------
        Name : string
            A unique plate name
        i_node : Node3D
            The plate's i-node
        j_node : Node3D
            The plate's j-node
        m_node : Node3D
            The plate's m-node
        n_node : Node3D
            The plate's n-node
        t : number
            Plate thickness
        E : number
            Plate modulus of elasticity
        nu : number
            Poisson's ratio
        LoadCombos : dict {combo_name: LoacCombo}
            A dictionary of the load combinations used in the model the plate is in
        
        """

        self.Name = Name
        self.ID = None
        self.type = 'Rect'

        self.i_node = i_node
        self.j_node = j_node
        self.m_node = m_node
        self.n_node = n_node

        self.t = t
        self.E = E
        self.nu = nu

        self.pressures = []  # A list of surface pressures [pressure, case='Case 1']
        self.LoadCombos = LoadCombos
    
    def width(self):
        """
        Returns the width of the plate along its local x-axis
        """
        return ((self.j_node.X - self.i_node.X)**2 + (self.j_node.Y - self.i_node.Y)**2 + (self.j_node.Z - self.i_node.Z)**2)**0.5

    def height(self):
        """
        Returns the height of the plate along its local y-axis
        """
        return ((self.n_node.X - self.i_node.X)**2 + (self.n_node.Y - self.i_node.Y)**2 + (self.n_node.Z - self.i_node.Z)**2)**0.5

    def k(self):
        """
        returns the plate's local stiffness matrix
        """
        return add(self.k_b(), self.k_m())
    
    def k_b(self):
        """
        Returns the local stiffness matrix for bending
        """

        a = self.width()
        b = self.height()
        beta = b/a

        E = self.E
        t = self.t
        nu = self.nu

        # Stiffness matrix for plate bending
        k = matrix([[4*(beta**2+beta**(-2))+1/5*(14-4*nu),    0,                                 0,                              0,                                       0,                                 0,                               0,                                      0,                                 0,                              0,                                    0,                                  0],
                    [(2*beta**(-2)+1/5*(1+4*nu))*b,           (4/3*beta**(-2)+4/15*(1-nu))*b**2, 0,                              0,                                       0,                                 0,                               0,                                      0,                                 0,                              0,                                    0,                                  0],
                    [-(2*beta**2+1/5*(1+4*nu))*a,             -nu*a*b,                           (4/3*beta**2+4/15*(1-nu))*a**2, 0,                                       0,                                 0,                               0,                                      0,                                 0,                              0,                                    0,                                  0],
                    [2*(beta**2-2*beta**(-2))-1/5*(14-4*nu),  -(2*beta**(-2)+1/5*(1-nu))*b,      (-beta**2+1/5*(1+4*nu))*a,      4*(beta**2+beta**(-2))+1/5*(14-4*nu),    0,                                 0,                               0,                                      0,                                 0,                              0,                                    0,                                  0],
                    [(2*beta**(-2)+1/5*(1-nu))*b,             (2/3*beta**(-2)-1/15*(1-nu))*b**2, 0,                              -(2*beta**(-2)+1/5*(1+4*nu))*b,          (4/3*beta**(-2)+4/15*(1-nu))*b**2, 0,                               0,                                      0,                                 0,                              0,                                    0,                                  0],
                    [(-beta**2+1/5*(1+4*nu))*a,               0,                                 (2/3*beta**2-4/15*(1-nu))*a**2, -(2*beta**2+1/5*(1+4*nu))*a,             nu*a*b,                            (4/3*beta**2+4/15*(1-nu))*a**2,  0,                                      0,                                 0,                              0,                                    0,                                  0],
                    [-2*(beta**2+beta**(-2))+1/5*(14-4*nu),   (-beta**(-2)+1/5*(1-nu))*b,        (beta**2-1/5*(1-nu))*a,         -2*(2*beta**2-beta**(-2))-1/5*(14-4*nu), (-beta**(-2)+1/5*(1+4*nu))*b,      (2*beta**2+1/5*(1-nu))*a,        4*(beta**2+beta**(-2))+1/5*(14-4*nu),   0,                                 0,                              0,                                    0,                                  0],
                    [(beta**(-2)-1/5*(1-nu))*b,               (1/3*beta**(-2)+1/15*(1-nu))*b**2, 0,                              (-beta**(-2)+1/5*(1+4*nu))*b,            (2/3*beta**(-2)-4/15*(1-nu))*b**2, 0,                               -(2*beta**(-2)+1/5*(1+4*nu))*b,         (4/3*beta**(-2)+4/15*(1-nu))*b**2, 0,                              0,                                    0,                                  0],
                    [(-beta**2+1/5*(1-nu))*a,                 0,                                 (1/3*beta**2+1/15*(1-nu))*a**2, -(2*beta**2+1/5*(1-nu))*a,               0,                                 (2/3*beta**2-1/15*(1-nu))*a**2,  (2*beta**2+1/5*(1+4*nu))*a,             -nu*a*b,                           (4/3*beta**2+4/15*(1-nu))*a**2, 0,                                    0,                                  0],
                    [-2*(2*beta**2-beta**(-2))-1/5*(14-4*nu), (beta**(-2)-1/5*(1+4*nu))*b,       (2*beta**2+1/5*(1-nu))*a,       -2*(beta**2+beta**(-2))+1/5*(14-4*nu),   (beta**(-2)-1/5*(1-nu))*b,         (beta**2-1/5*(1-nu))*a,          2*(beta**2-2*beta**(-2))-1/5*(14-4*nu), (2*beta**(-2)+1/5*(1-nu))*b,       (beta**2-1/5*(1+4*nu))*a,       4*(beta**2+beta**(-2))+1/5*(14-4*nu), 0,                                  0],
                    [(beta**(-2)-1/5*(1+4*nu))*b,             (2/3*beta**(-2)-4/15*(1-nu))*b**2, 0,                              (-beta**(-2)+1/5*(1-nu))*b,              (1/3*beta**(-2)+1/15*(1-nu))*b**2, 0,                               -(2*beta**(-2)+1/5*(1-nu))*b,           (2/3*beta**(-2)-1/15*(1-nu))*b**2, 0,                              (2*beta**(-2)+1/5*(1+4*nu))*b,        (4/3*beta**(-2)+4/15*(1-nu))*b**2,  0],
                    [-(2*beta**2+1/5*(1-nu))*a,               0,                                 (2/3*beta**2-1/15*(1-nu))*a**2, (-beta**2+1/5*(1-nu))*a,                 0,                                 (1/3*beta**2+1/15*(1-nu))*a**2,  (beta**2-1/5*(1+4*nu))*a,               0,                                 (2/3*beta**2-4/15*(1-nu))*a**2, (2*beta**2+1/5*(1+4*nu))*a,           nu*a*b,                             (4/3*beta**2+4/15*(1-nu))*a**2]])

        k = k*E*t**3/(12*(1-nu**2)*a*b)

        # Apply symmetry to the matrix
        for i in range(12):
            for j in range(i, 12):
                k[i, j] = k[j, i]
        
        # Calculate the stiffness of a weak spring for the drilling degree of freedom (rotation
        # about local z). We'll set the weak spring to be 1000 times weaker than any of the other
        # rotational stiffnesses in the matrix.
        k_rz = min(abs(k[1, 1]), abs(k[2, 2]), abs(k[4, 4]), abs(k[5, 5]),
                   abs(k[7, 7]), abs(k[8, 8]), abs(k[10, 10]), abs(k[11, 11])
                   )/1000

        # The matrix currently only holds terms related to bending action. We need to expand it to
        # with placeholders for all the degrees of freedom so it can be directly added to the
        # membrane stiffness matrix later on.

        # Initialize the expanded stiffness matrix to all zeros
        k_exp = zeros((24, 24))

        # Step through each term in the unexpanded stiffness matrix

        # i = Unexpanded matrix row
        for i in range(12):

            # j = Unexpanded matrix column
            for j in range(12):
                
                # Find the corresponding term in the expanded stiffness
                # matrix

                # m = Expanded matrix row
                if i in [0, 3, 6, 9]:  # indices associated with deflection in z
                    m = 2*i + 2
                if i in [1, 4, 7, 10]:  # indices associated with rotation about x
                    m = 2*i + 1
                if i in [2, 5, 8, 11]:  # indices associated with rotation about y
                    m = 2*i

                # n = Expanded matrix column
                if j in [0, 3, 6, 9]:  # indices associated with deflection in z
                    n = 2*j + 2
                if j in [1, 4, 7, 10]:  # indices associated with rotation about x
                    n = 2*j + 1
                if j in [2, 5, 8, 11]:  # indices associated with rotation about y
                    n = 2*j
                
                # Ensure the indices are integers rather than floats
                m, n = round(m), round(n)

                # Add the term from the unexpanded matrix into the expanded
                # matrix
                k_exp[m, n] = k[i, j]
        
        # Add the drilling degree of freedom's weak spring
        k_exp[5, 5] = k_rz
        k_exp[11, 11] = k_rz
        k_exp[17, 17] = k_rz
        k_exp[23, 23] = k_rz
        
        # Return the local stiffness matrix
        return k_exp

    def k_m(self):
        """
        Returns the local stiffness matrix for membrane forces
        """

        a = self.width()
        b = self.height()
        beta = b/a
        
        E = self.E
        t = self.t
        nu = self.nu
        
        k = matrix([[4*beta+2*(1-nu)*beta**(-1), 0,                          0,                          0,                          0,                          0,                          0,                          0],
                    [3/2*(1+nu),                 4*beta**(-1)+2*(1-nu)*beta, 0,                          0,                          0,                          0,                          0,                          0],
                    [2*beta-2*(1-nu)*beta**(-1), -3/2*(1-3*nu),              4*beta+2*(1-nu)*beta**(-1), 0,                          0,                          0,                          0,                          0],
                    [3/2*(1-3*nu),               -4*beta**(-1)+(1-nu)*beta,  -3/2*(1+nu),                4*beta**(-1)+2*(1-nu)*beta, 0,                          0,                          0,                          0],
                    [-2*beta-(1-nu)*beta**(-1),  -3/2*(1+nu),                -4*beta+(1-nu)*beta**(-1),  -3/2*(1-3*nu),              4*beta+2*(1-nu)*beta**(-1), 0,                          0,                          0],
                    [-3/2*(1+nu),                -2*beta**(-1)-(1-nu)*beta,  3/2*(1-3*nu),               2*beta**(-1)-2*(1-nu)*beta, 3/2*(1+nu),                 4*beta**(-1)+2*(1-nu)*beta, 0,                          0],
                    [-4*beta+(1-nu)*beta**(-1),  3/2*(1-3*nu),               -2*beta-(1-nu)*beta**(-1),  3/2*(1+nu),                 2*beta-2*(1-nu)*beta**(-1), -3/2*(1-3*nu),              4*beta+2*(1-nu)*beta**(-1), 0],
                    [-3/2*(1-3*nu),              2*beta**(-1)-2*(1-nu)*beta, 3/2*(1+nu),                 -2*beta**(-1)-(1-nu)*beta,  3/2*(1-3*nu),               -4*beta**(-1)+(1-nu)*beta,  -3/2*(1+nu),                4*beta**(-1)+2*(1-nu)*beta]])
        
        k = k*E*t/(12*(1-nu**2))

        # Apply symmetry to the matrix
        for i in range(8):
            for j in range(i, 8):
                k[i, j] = k[j, i]
        
        # At this point `k` only contains terms for the degrees of freedom
        # associated with membrane action. Expand `k` to include zero terms for
        # the degrees of freedom related to bending forces. This will allow
        # the bending and membrane stiffness matrices to be summed directly
        # later on. `numpy` has an `insert` function that can be used to
        # insert rows and columns of zeros one at a time, but it is very slow
        # as it makes a temporary copy of the matrix term by term each time
        # it's called. The algorithm used here accomplishes the same thing
        # much faster. Terms are copied only once.
        k_exp = zeros((24, 24))

        # Step through each term in the unexpanded stiffness matrix

        # i = Unexpanded matrix row
        for i in range(8):

            # j = Unexpanded matrix column
            for j in range(8):
                
                # Find the corresponding term in the expanded stiffness
                # matrix

                # m = Expanded matrix row
                if i in [0, 2, 4, 6]:  # indices associated with displacement in x
                    m = i*3
                if i in [1, 3, 5, 7]:  # indices associated with displacement in y
                    m = i*3 - 2

                # n = Expanded matrix column
                if j in [0, 2, 4, 6]:  # indices associated with displacement in x
                    n = j*3
                if j in [1, 3, 5, 7]:  # indices associated with displacement in y
                    n = j*3 - 2
                
                # Ensure the indices are integers rather than floats
                m, n = round(m), round(n)

                # Add the term from the unexpanded matrix into the expanded
                # matrix
                k_exp[m, n] = k[i, j]
        
        return k_exp
  
    def f(self, combo_name='Combo 1'):
        """
        Returns the plate's local end force vector
        """
        
        # Calculate and return the plate's local end force vector
        return add(matmul(self.k(), self.d(combo_name)), self.fer(combo_name))

    def fer(self, combo_name='Combo 1'):
        """
        Returns the rectangle's local fixed end reaction vector.

        Parameters
        ----------
        combo_name : string
            The name of the load combination to get the load vector for.
        """
        
        # Initialize the fixed end reaction vector
        fer = zeros((12, 1))

        # Get the requested load combination
        combo = self.LoadCombos[combo_name]

        # Initialize the element's surface pressure to zero
        p = 0
        
        # Loop through each load case and factor in the load combination 
        for case, factor in combo.factors.items():

            # Sum the pressures
            for pressure in self.pressures:

                # Check if the current pressure corresponds to the current load case
                if pressure[1] == case:

                    # Sum the pressures multiplied by their load factors
                    p += factor*pressure[0]
        
        b = self.width()/2
        c = self.height()/2
        
        fer = -4*p*c*b*array([[1/4], [c/12], [-b/12], [1/4], [-c/12], [-b/12], [1/4], [-c/12], [b/12], [1/4], [c/12], [b/12]])

        # At this point `fer` only contains terms for the degrees of freedom
        # associated with membrane action. Expand `fer` to include zero terms for
        # the degrees of freedom related to bending action. This will allow
        # the bending and membrane vectors to be summed directly
        # later on. `numpy` has an `insert` function that can be used to
        # insert rows and columns of zeros one at a time, but it is very slow
        # as it makes a temporary copy of the vector term by term each time
        # it's called. The algorithm used here accomplishes the same thing
        # much faster. Terms are copied only once.

        # Initialize the expanded vector to all zeros
        fer_exp = zeros((24, 1))

        # Step through each term in the unexpanded vector
        # i = Unexpanded vector row
        for i in range(12):
                
            # Find the corresponding term in the expanded vector

            # m = Expanded vector row
            if i in [0, 3, 6, 9]:   # indices associated with deflection in z
                m = 2*i + 2
            if i in [1, 4, 7, 10]:  # indices associated with rotation about x
                m = 2*i + 1
            if i in [2, 5, 8, 11]:  # indices associated with rotation about y
                m = 2*i
                
            # Ensure the index is an integer rather than a float
            m = round(m)

            # Add the term from the unexpanded vector into the expanded vector
            fer_exp[m, 0] = fer[i, 0]

        return fer_exp
        
    def d(self, combo_name='Combo 1'):
       """
       Returns the plate's local displacement vector
       """

       # Calculate and return the local displacement vector
       return matmul(self.T(), self.D(combo_name))

    def F(self, combo_name='Combo 1'):
        """
        Returns the plate's global nodal force vector
        """

        # Calculate and return the global force vector
        return matmul(inv(self.T()), self.f(combo_name))

    def D(self, combo_name='Combo 1'):
        """
        Returns the plate's global displacement vector for the given load combination.
        """
        
        # Initialize the displacement vector
        D = zeros((24, 1))
        
        # Read in the global displacements from the nodes
        D.itemset((0, 0), self.i_node.DX[combo_name])
        D.itemset((1, 0), self.i_node.DY[combo_name])
        D.itemset((2, 0), self.i_node.DZ[combo_name])
        D.itemset((3, 0), self.i_node.RX[combo_name])
        D.itemset((4, 0), self.i_node.RY[combo_name])
        D.itemset((5, 0), self.i_node.RZ[combo_name])

        D.itemset((6, 0), self.n_node.DX[combo_name])
        D.itemset((7, 0), self.n_node.DY[combo_name])
        D.itemset((8, 0), self.n_node.DZ[combo_name])
        D.itemset((9, 0), self.n_node.RX[combo_name])
        D.itemset((10, 0), self.n_node.RY[combo_name])
        D.itemset((11, 0), self.n_node.RZ[combo_name])

        D.itemset((12, 0), self.m_node.DX[combo_name])
        D.itemset((13, 0), self.m_node.DY[combo_name])
        D.itemset((14, 0), self.m_node.DZ[combo_name])
        D.itemset((15, 0), self.m_node.RX[combo_name])
        D.itemset((16, 0), self.m_node.RY[combo_name])
        D.itemset((17, 0), self.m_node.RZ[combo_name])

        D.itemset((18, 0), self.j_node.DX[combo_name])
        D.itemset((19, 0), self.j_node.DY[combo_name])
        D.itemset((20, 0), self.j_node.DZ[combo_name])
        D.itemset((21, 0), self.j_node.RX[combo_name])
        D.itemset((22, 0), self.j_node.RY[combo_name])
        D.itemset((23, 0), self.j_node.RZ[combo_name])
        
        # Return the global displacement vector
        return D
 
    def T(self):
        """
        Returns the plate's transformation matrix
        """

        # Calculate the direction cosines for the local x-axis
        # The local x-axis will run from the i-node to the j-node
        xi = self.i_node.X
        xj = self.j_node.X
        yi = self.i_node.Y
        yj = self.j_node.Y
        zi = self.i_node.Z
        zj = self.j_node.Z
        x = [(xj - xi), (yj - yi), (zj - zi)]
        x = x/norm(x)
        
        # The local y-axis will be in the plane of the plate
        # Find a vector in the plate's local xy plane
        xn = self.n_node.X
        yn = self.n_node.Y
        zn = self.n_node.Z
        xy = [xn - xi, yn - yi, zn - zi]

        # Find a vector perpendicular to the plate surface to get the orientation of the local z-axis
        z = cross(x, xy)
        
        # Divide the vector by its magnitude to produce a unit z-vector of direction cosines
        z = z/norm(z)

        # Calculate the local y-axis as a vector perpendicular to the local z and x-axes
        y = cross(z, x)
        
        # Divide the z-vector by its magnitude to produce a unit vector of direction cosines
        y = y/norm(y)

        # Create the direction cosines matrix
        dirCos = array([x, y, z])
        
        # Build the transformation matrix
        transMatrix = zeros((24, 24))
        transMatrix[0:3, 0:3] = dirCos
        transMatrix[3:6, 3:6] = dirCos
        transMatrix[6:9, 6:9] = dirCos
        transMatrix[9:12, 9:12] = dirCos
        transMatrix[12:15, 12:15] = dirCos
        transMatrix[15:18, 15:18] = dirCos
        transMatrix[18:21, 18:21] = dirCos
        transMatrix[21:24, 21:24] = dirCos
        
        return transMatrix

    def K(self):
        """
        Returns the plate's global stiffness matrix
        """

        # Calculate and return the stiffness matrix in global coordinates
        return matmul(matmul(inv(self.T()), self.k()), self.T())

    def FER(self, combo_name='Combo 1'):
        """
        Returns the global fixed end reaction vector.

        Parameters
        ----------
        combo_name : string
            The name of the load combination to calculate the fixed end
            reaction vector for (not the load combination itself).
        """
        
        # Calculate and return the fixed end reaction vector
        return matmul(inv(self.T()), self.fer(combo_name))

    def _C(self):
        """
        Returns the plate's displacement coefficient matrix [C]
        """

        # Find the local x and y coordinates at each node
        xi = 0
        yi = 0
        xj = self.width()
        yj = 0
        xm = xj
        ym = self.height()
        xn = 0
        yn = ym

        # Calculate the [C] coefficient matrix
        C = matrix([[1, xi, yi, xi**2, xi*yi, yi**2, xi**3, xi**2*yi, xi*yi**2, yi**3, xi**3*yi, xi*yi**3],
                    [0, 0, 1, 0, xi, 2*yi, 0, xi**2, 2*xi*yi, 3*yi**2, xi**3, 3*xi*yi**2],
                    [0, -1, 0, -2*xi, -yi, 0, -3*xi**2, -2*xi*yi, -yi**2, 0, -3*xi**2*yi, -yi**3],
                    
                    [1, xn, yn, xn**2, xn*yn, yn**2, xn**3, xn**2*yn, xn*yn**2, yn**3, xn**3*yn, xn*yn**3],
                    [0, 0, 1, 0, xn, 2*yn, 0, xn**2, 2*xn*yn, 3*yn**2, xn**3, 3*xn*yn**2],
                    [0, -1, 0, -2*xn, -yn, 0, -3*xn**2, -2*xn*yn, -yn**2, 0, -3*xn**2*yn, -yn**3],

                    [1, xm, ym, xm**2, xm*ym, ym**2, xm**3, xm**2*ym, xm*ym**2, ym**3, xm**3*ym, xm*ym**3],
                    [0, 0, 1, 0, xm, 2*ym, 0, xm**2, 2*xm*ym, 3*ym**2, xm**3, 3*xm*ym**2],
                    [0, -1, 0, -2*xm, -ym, 0, -3*xm**2, -2*xm*ym, -ym**2, 0, -3*xm**2*ym, -ym**3],

                    [1, xj, yj, xj**2, xj*yj, yj**2, xj**3, xj**2*yj, xj*yj**2, yj**3, xj**3*yj, xj*yj**3],
                    [0, 0, 1, 0, xj, 2*yj, 0, xj**2, 2*xj*yj, 3*yj**2, xj**3, 3*xj*yj**2],
                    [0, -1, 0, -2*xj, -yj, 0, -3*xj**2, -2*xj*yj, -yj**2, 0, -3*xj**2*yj, -yj**3]])

        # Return the coefficient matrix
        return C

    def _Q(self, x, y):
        """
        Calculates and returns the plate curvature coefficient matrix [Q] at a given point (x, y)
        in the plate's local system.
        """

        # Calculate the [Q] coefficient matrix
        Q = matrix([[0, 0, 0, -2, 0, 0, -6*x, -2*y, 0, 0, -6*x*y, 0],
                    [0, 0, 0, 0, 0, -2, 0, 0, -2*x, -6*y, 0, -6*x*y],
                    [0, 0, 0, 0, -2, 0, 0, -4*x, -4*y, 0, -6*x**2, -6*y**2]])
        
        # Return the [Q] coefficient matrix
        return Q

    def _a(self, combo_name='Combo 1'):
        """
        Returns the vector of plate bending constants for the displacement function.

        Parameters
        ----------
        combo_name : string
            The name of the load combination to get the vector for
        """

        # Get the plate's local displacement vector
        # Slice out terms not related to plate bending
        d = self.d(combo_name)[[2, 3, 4, 8, 9, 10, 14, 15, 16, 20, 21, 22], :]

        # Return the plate bending constants
        return inv(self._C())*d

    def _D(self):
        """
        Calculates and returns the constitutive matrix for isotropic materials [D].
        """

        # Calculate the coefficient for the constitutive matrix [D]
        nu = self.nu
        C = self.E*self.t**3/(12*(1 - nu**2))

        # Calculate the constitutive matrix [D]
        D = C*matrix([[1, nu, 0],
                      [nu, 1, 0],
                      [0, 0, (1-nu)/2]])

        # Return the constitutive matrix [D]
        return D

    def moment(self, x, y, combo_name='Combo 1'):
        """
        Returns the internal moments (Mx, My, and Mxy) at any point (x, y) in the plate's local
        coordinate system

        Parameters
        ----------
        x : number
            The x-coordinate in the plate's local coordinate system.
        y : number
            The y-coordinate in the plate's local coordinate system.
        combo_name : string
            The name of the load combination to evaluate. The default is 'Combo 1'.

        """
        
        # Calculate and return internal moments
        # A negative sign will be applied to change the sign convention to match that of
        # PyNite's quadrilateral elements.
        return -self._D()*self._Q(x, y)*self._a(combo_name)
 
    def shear(self, x, y, combo_name='Combo 1'):
        """
        Returns the internal shears (Qx and Qy) at any point (x, y) in the plate's local
        coordinate system

        Parameters
        ----------
        x : number
            The x-coordinate in the plate's local coordinate system.
        y : number
            The y-coordinate in the plate's local coordinate system.
        combo_name : string
            The name of the load combination to evaluate. The default is 'Combo 1'.

        """

        # Store matrices into local variables for quicker access
        D = self._D()
        a = self._a(combo_name)

        # Calculate the derivatives of the plate moments needed to compute shears
        dMx_dx = (D*matrix([[0, 0, 0, 0, 0, 0, -6, 0, 0, 0, -6*y, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, -2, 0, 0, -6*y],
                            [0, 0, 0, 0, 0, 0, 0, -4, 0, 0, -12*x, 0]])*a)[0]

        dMxy_dy = (D*matrix([[0, 0, 0, 0, 0, 0, 0, -2, 0, 0, -6*x, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, -6, 0, -6*x],
                             [0, 0, 0, 0, 0, 0, 0, 0, -4, 0, 0, -12*y]])*a)[2]
        
        dMy_dy = (D*matrix([[0, 0, 0, 0, 0, 0, 0, -2, 0, 0, -6*x, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, -6, 0, -6*x],
                            [0, 0, 0, 0, 0, 0, 0, 0, -4, 0, 0, -12*y]])*a)[1]

        dMxy_dx = (D*matrix([[0, 0, 0, 0, 0, 0, -6, 0, 0, 0, -6*y, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, -2, 0, 0, -6*y],
                             [0, 0, 0, 0, 0, 0, 0, -4, 0, 0, -12*x, 0]])*a)[2]
        
        # Calculate internal shears
        Qx = (dMx_dx + dMxy_dy)[0, 0]
        Qy = (dMy_dy + dMxy_dx)[0, 0]

        # Return internal shears
        return matrix([[Qx], 
                       [Qy]])

    def membrane(self, x, y, combo_name='Combo 1'):
        """
        Returns the in-plane (membrane) stresses in the plate.

        Parameters
        ----------
        x : number
            The plate's local x-coordinate where stresses will be calculated.
        y : number
            The plate's local y-coordinate where stresses will be calculated.
        combo_name : string, optional
            The name of the load combination to get stresses for. The default is 'Combo 1'.

        Returns
        -------
        array
            An array of the local in-plane stresses in the format [[Sx, Sy, Txy]].
        
        """

        # Get the plate's local displacement vector
        # Slice out terms not related to membrane forces
        d = self.d(combo_name)[[0, 1, 6, 7, 12, 13, 18, 19], :]
        
        a = self.width()
        b = self.height()

        eta = y/b
        epsilon = x/a
        nu = self.nu
        E = self.E

        return E/(1-nu**2)*matmul(array([[-(1-eta)/a,                -nu*(1-epsilon)/b,     -eta/a,                   nu*(1-epsilon)/b,  eta/a,                nu*epsilon/b,     (1-eta)/a,             -nu*epsilon/b],
                                         [-nu*(1-eta)/a,             -(1-epsilon)/b,        -nu*eta/a,                (1-epsilon)/b,     nu*eta/a,             epsilon/b,        nu*(1-eta)/a,          -epsilon/b],
                                         [-(1-nu)*(1-epsilon)/(2*b), -(1-nu)*(1-eta)/(2*a), (1-nu)*(1-epsilon)/(2*b), -(1-nu)*eta/(2*a), (1-nu)*epsilon/(2*b), (1-nu)*eta/(2*a), -(1-nu)*epsilon/(2*b), (1-nu)*(1-eta)/(2*a)]]), d)
