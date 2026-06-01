import pyomo.environ as pyo
from pyomo.opt import SolverStatus, TerminationCondition

MATERIAS = [
    
    "Adquisición y Análisis de Datos",
    "Estructuras de Datos",
    "Metodologías de la Investigación",
    "Metodologías Ágiles",
    "Conocimiento y Razonamiento Automático",
    "Optimización",
]

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
BLOQUES = [1, 2, 3, 4]  # 4 bloques de 2 horas por día

def resolver_estudios(bloques_bloqueados, prioridades, min_horas=6, max_bloques_dia=3):
    """
    bloques_bloqueados: lista de tuplas (dia, bloque) que no están disponibles
    prioridades: dict {materia: peso} entre 0 y 1
    min_horas: horas mínimas por materia por semana
    max_bloques_dia: máximo de bloques de estudio por día
    """

    model = pyo.ConcreteModel()

    # Variables binarias: x[dia, bloque, materia] = 1 si estudias esa materia
    model.x = pyo.Var(DIAS, BLOQUES, MATERIAS, domain=pyo.Binary)

    # Función objetivo: maximizar bloques ponderados por prioridad
    model.objetivo = pyo.Objective(
        expr=sum(
            prioridades[m] * model.x[d, b, m]
            for d in DIAS
            for b in BLOQUES
            for m in MATERIAS
        ),
        sense=pyo.maximize
    )

    model.r = pyo.ConstraintList()

    # 1. En cada bloque solo se puede estudiar una materia
    for d in DIAS:
        for b in BLOQUES:
            model.r.add(
                sum(model.x[d, b, m] for m in MATERIAS) <= 1
            )

    # 2. Cada materia debe tener mínimo de bloques por semana
    # min_horas / 2 horas por bloque = bloques mínimos
    bloques_minimos = min_horas // 2
    for m in MATERIAS:
        model.r.add(
            sum(model.x[d, b, m] for d in DIAS for b in BLOQUES) >= bloques_minimos
        )

    # 3. Bloques bloqueados no se pueden usar
    for (d, b) in bloques_bloqueados:
        model.r.add(
            sum(model.x[d, b, m] for m in MATERIAS) == 0
        )

    # 4. Máximo de bloques de estudio por día
    for d in DIAS:
        model.r.add(
            sum(model.x[d, b, m] for b in BLOQUES for m in MATERIAS) <= max_bloques_dia
        )

    # 5. Máximo de bloques por materia (máximo el doble del mínimo)
    bloques_maximos = bloques_minimos * 2
    for m in MATERIAS:
        model.r.add(
        sum(model.x[d, b, m] for d in DIAS for b in BLOQUES) <= bloques_maximos
        )

    # Resolver
    solver = pyo.SolverFactory("glpk")
    resultado = solver.solve(model)

    if (resultado.solver.status == SolverStatus.ok and
            resultado.solver.termination_condition == TerminationCondition.optimal):

        # Construir calendario
        calendario = {}
        for d in DIAS:
            calendario[d] = {}
            for b in BLOQUES:
                asignado = None
                for m in MATERIAS:
                    if pyo.value(model.x[d, b, m]) > 0.5:
                        asignado = m
                calendario[d][b] = asignado

        # Contar horas por materia
        horas_por_materia = {}
        for m in MATERIAS:
            bloques_asignados = sum(
                pyo.value(model.x[d, b, m])
                for d in DIAS for b in BLOQUES
            )
            horas_por_materia[m] = round(bloques_asignados * 2, 1)

        # Calcular bloques libres por día para M4
        bloques_libres = {}
        for d in DIAS:
            libres = sum(
                1 for b in BLOQUES
                if calendario[d][b] is None and (d, b) not in bloques_bloqueados
            )
            bloques_libres[d] = libres

        return {
            "estado": "optimo",
            "calendario": calendario,
            "horas_por_materia": horas_por_materia,
            "bloques_libres": bloques_libres,
        }
    else:
        return {"estado": "infactible"}