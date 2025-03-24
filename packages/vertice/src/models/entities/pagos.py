class Pago():
    def __init__(self, id=None, cedula_estudiante=None, metodo_pago_id=None, monto_id=None,
                 fecha_pago=None, referencia_transferencia=None, ciclo=None):
        self.id = id
        self.cedula_estudiante = cedula_estudiante
        self.metodo_pago_id = metodo_pago_id
        self.monto_id = monto_id
        self.fecha_pago = fecha_pago
        self.referencia_transferencia = referencia_transferencia
        self.ciclo = ciclo
    
    def to_JSON(self):
        return {
            "id": self.id,
            "estudiante": self.cedula_estudiante,  
            "metodo_pago": self.metodo_pago_id.to_JSON(),
            "monto": self.monto_id.to_JSON(),
            "fecha_pago": self.fecha_pago,
            "referencia_transferencia": self.referencia_transferencia,
            "ciclo": self.ciclo
        }
