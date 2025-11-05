/** @odoo-module **/

import { ProjectTaskStateSelection } from "@project/src/components/project_task_state_selection/project_task_state_selection";
import { stateSelectionField } from "@web/views/fields/state_selection/state_selection_field";
import { registry } from "@web/core/registry";

export class ProjectTaskStateSelectionInherit extends ProjectTaskStateSelection {
    setup() {
        super.setup();

        // 👉 Añadimos configuración visual para el nuevo estado
        this.icons["04_waiting_feedback"] = "fa fa-lg fa-question-circle";
        this.colorIcons["04_waiting_feedback"] = "text-warning";
        this.colorButton["04_waiting_feedback"] = "btn-outline-warning";
    }

    // 👉 Sobrescribimos el método options para que incluya nuestro estado
    get options() {
        const baseOptions = super.options;
        const labels = new Map(baseOptions);

        // lógica original de Odoo
        const states = ["1_canceled", "1_done"];
        const currentState = this.props.record.data[this.props.name];
        if (currentState != "04_waiting_normal") {
            states.unshift("01_in_progress", "02_changes_requested", "03_approved");
        }

        // añadimos nuestro estado personalizado
        states.push("04_waiting_feedback");

        return states
            .filter((state) => labels.has(state))
            .map((state) => [state, labels.get(state)]);
    }
}

// ⚡ Reemplazamos el widget en el registry
registry.category("fields").add("project_task_state_selection", {
    ...stateSelectionField,
    component: ProjectTaskStateSelectionInherit,
    fieldDependencies: [{ name: "project_id", type: "many2one" }],
    supportedOptions: [
        ...stateSelectionField.supportedOptions,
        {
            label: "Is toggle mode",
            name: "is_toggle_mode",
            type: "boolean",
        },
    ],
    extractProps({ options, viewType }) {
        const props = stateSelectionField.extractProps(...arguments);
        props.isToggleMode = Boolean(options.is_toggle_mode);
        props.viewType = viewType;
        return props;
    },
});
