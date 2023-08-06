__version__='0.0.1'

class viewport:

    def __init__( self, Wb=0, Wt=1, Wl=0, Wr=1, Vb=-1, Vt=1, Vl=-1, Vr=1 ):
        self.Sx = ( Vr - Vl ) / ( Wr - Wl )
        self.Sy = ( Vt - Vb ) / ( Wt - Wb );
        self.Tx = ( Vl * Wr - Wl * Vr ) / ( Wr - Wl );
        self.Ty = ( Vb * Wt - Wb * Vt ) / ( Wt - Wb );

    def Dx( self, x ):
        return self.Sx * x + self.Tx

    def Dy( self, y ):
        return self.Sy * y + self.Ty
