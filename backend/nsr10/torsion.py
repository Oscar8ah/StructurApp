def evaluar_torsion_piso(delta1, delta2):
    delta_max = max(delta1, delta2)
    delta_min = min(delta1, delta2)
    promedio = (delta1 + delta2) / 2.0
    limite_1ap = 1.2 * promedio
    limite_1bp = 1.4 * promedio
    irreg_1ap = (delta_max > limite_1ap) and (delta_max <= limite_1bp)
    irreg_1bp = delta_max > limite_1bp

    if irreg_1bp:
        phi_p = 0.80
    elif irreg_1ap:
        phi_p = 0.90
    else:
        phi_p = 1.00

    return {
        "delta_max_cm": round(delta_max, 4),
        "delta_min_cm": round(delta_min, 4),
        "promedio_cm": round(promedio, 4),
        "limite_1aP_cm": round(limite_1ap, 4),
        "limite_1bP_cm": round(limite_1bp, 4),
        "irregularidad_1aP": irreg_1ap,
        "irregularidad_1bP": irreg_1bp,
        "phi_p": phi_p,
        "resultado": "1bP" if irreg_1bp else ("1aP" if irreg_1ap else "Regular"),
    }

def evaluar_torsion_proyecto(pisos_datos):
    resultados = []
    for piso in pisos_datos:
        res = evaluar_torsion_piso(piso["delta1_cm"], piso["delta2_cm"])
        resultados.append({
            "piso": piso["piso"],
            "direccion_sismo": piso["direccion_sismo"],
            "par_nodos": piso["par_nodos"],
            **res,
        })

    phi_p_global = min(r["phi_p"] for r in resultados)
    tiene_1ap = any(r["irregularidad_1aP"] for r in resultados)
    tiene_1bp = any(r["irregularidad_1bP"] for r in resultados)

    return {
        "phi_p_global": phi_p_global,
        "tiene_1aP": tiene_1ap,
        "tiene_1bP": tiene_1bp,
        "clasificacion": "Irregular" if (tiene_1ap or tiene_1bp) else "Regular",
        "detalle_por_piso": resultados,
    }