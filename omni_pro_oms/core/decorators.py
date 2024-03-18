from omni_pro_oms.models import Task


def task_flow_register(func):
    """
    Decorador diseñado para registrar el flujo de una tarea, manejar su éxito o fracaso,
    y en caso de fallo, lanzar una excepción. La función decorada debe retornar una tupla
    que contiene un objeto de respuesta (puede ser un diccionario vacío) y una tupla `_t`.
    La tupla `_t` debe contener un mensaje, un valor booleano indicando el éxito, y datos de la
    solicitud (`rq`) en ese orden.

    La ejecución exitosa o fallida de la función decorada determina si se lanza una excepción
    y cómo se registra el paso en el objeto de tarea asociado.

    Parameters:
        func (Callable): La función a decorar. Debe retornar una tupla con la forma (response, _t),
                         donde '_t' es otra tupla de la forma (message, success, rq).

    Returns:
        Callable: Una función wrapper que envuelve a `func`, gestionando la captura y registro de
                  su ejecución dentro del flujo de una tarea específica.

    Raises:
        Exception: Si `success` en la tupla `_t` retornada por `func` es False, se levanta una excepción
                   con el `message` contenido en `_t`.

    Example:
        @task_flow_register
        def mi_funcion_de_tarea(task, rq_data):
            # Lógica de la función...
            return {}, ("Operación exitosa", True, rq_data)

    Note:
        - Es crucial que la función decorada cumpla con la estructura de retorno esperada.
        - El primer argumento de la función decorada debe tener un atributo `task` desde el cual
          se puedan registrar los detalles de la ejecución del paso.
    """

    def wrapper(*args, **kwargs):
        response, _t = func(*args, **kwargs)
        response = response or {}
        task: Task = args[0].task
        message, success, rq = _t
        step = {
            "success": success,
            "step_name": func.__name__.replace("_", " ").strip().upper(),
            "func_name": func.__name__,
            "message": message,
            "request": rq,
            "response": response,
        }
        task.response_dst.get("steps").append(step)
        task.save()
        if not success:
            raise Exception(message)
        return response, _t

    return wrapper
