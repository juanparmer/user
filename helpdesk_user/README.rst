Helpdesk User
=============

Este módulo integra los tickets de Helpdesk con las Tareas de Proyecto y los Partes de Horas, mejorando la trazabilidad y automatización para las actividades relacionadas con el soporte.

Características Principales
===========================

- Asocia automáticamente los tickets de helpdesk con los proyectos relacionados con el cliente.
- Crea automáticamente una tarea llamada "HelpDesk" para cada proyecto.
- Los tickets heredan la tarea del proyecto relacionado para los partes de horas.
- Previene que los partes de horas estén vinculados a una tarea y un ticket al mismo tiempo.
- Completa automáticamente los campos de proyecto y tarea en los partes de horas creados desde un ticket.
- Incluye una acción programada para generar tareas de HelpDesk faltantes en todos los proyectos.

Uso
===

1. **Crear o editar un proyecto**
   - Se creará automáticamente una tarea "HelpDesk" si no existe.

2. **Crear un ticket de helpdesk**
   - Al seleccionar un cliente, el sistema vincula el ticket con uno de sus proyectos activos.
   - Si no se encuentra ningún proyecto, se utiliza el proyecto predeterminado del equipo de helpdesk.
   - La tarea "HelpDesk" del proyecto se muestra, pero no es editable.

3. **Registrar partes de horas en tickets**
   - Los campos de proyecto y tarea se completan automáticamente.
   - No se puede vincular un parte de horas a una tarea y un ticket al mismo tiempo para evitar inconsistencias.

4. **Activar la Acción Programada (opcional)**
   - Ve a *Configuración > Técnico > Automatización > Acciones Programadas*.
   - Busca **D3: Crear Tarea HelpDesk** y actívala para poblar proyectos existentes con tareas de helpdesk.



Bug Tracker
-----------

Bugs are tracked on `GitHub Issues <https://github.com/TU_REPOSITORIO_GITHUB/issues>`_.
If you find a bug, please report it with detailed steps to reproduce the issue.


Credits
-------

Authors
~~~~~~~

.. image:: https://d-3system.com.au/wp-content/uploads/2020/05/Dimension3_Systems_460x159.png.webp
   :width: 25%
   :alt: Dimension 3 systems
   :target: https://d-3system.com.au/

Contributors
~~~~~~~~~~~~

* Juan Pablo Arcos

Maintainers
~~~~~~~~~~~

This module is maintained by your team or organization.

.. image:: https://d-3system.com.au/wp-content/uploads/2020/05/Dimension3_Systems_460x159.png.webp
   :width: 25%
   :alt: Dimension 3 systems
   :target: https://d-3system.com.au/

License
=======

Licensed under the LGPL v3.0 or later.  
This module is not part of an official OCA repository but follows OCA best development practices.
