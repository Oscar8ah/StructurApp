H_PISO_CM = 288.0
LIMITE_DERIVA_PCT = 0.01

def calcular_deriva_cm(drift, h_piso_cm=H_PISO_CM):
    return drift * h_piso_cm

def calcular_deriva_combinada(drift_x, drift_y, h_piso_cm=H_PISO_CM):
    dx = drift_x * h_piso_cm
    dy = drift_y * h_piso_cm
    return (dx**2 + dy**2) ** 0.5

def limite_deriva_cm(h_piso_cm=H_PISO_CM):
    return LIMITE_DERIVA_PCT * h_piso_cm

def procesar_derivas(datos_joints, h_piso_cm=H_PISO_CM):
    limite = limite_deriva_cm(h_piso_cm)
    resultado = []
    for r in datos_joints:
        dx_cm = calcular_deriva_cm(r["drift_x"], h_piso_cm)
        dy_cm = calcular_deriva_cm(r["drift_y"], h_piso_cm)
        combinada_cm = calcular_deriva_combinada(r["drift_x"], r["drift_y"], h_piso_cm)
        resultado.append({
            **r,
            "h_piso_cm": h_piso_cm,
            "deriva_x_cm": round(dx_cm, 4),
            "deriva_y_cm": round(dy_cm, 4),
            "deriva_combinada_cm": round(combinada_cm, 4),
            "limite_cm": round(limite, 4),
            "pct_x": round(dx_cm / h_piso_cm * 100, 4),
            "pct_y": round(dy_cm / h_piso_cm * 100, 4),
            "pct_combinado": round(combinada_cm / h_piso_cm * 100, 4),
            "cumple_x": dx_cm <= limite,
            "cumple_y": dy_cm <= limite,
            "cumple_combinado": combinada_cm <= limite,
        })
    return resultado