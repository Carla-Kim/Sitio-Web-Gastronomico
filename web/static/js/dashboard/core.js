/* =========================
    TABLES
========================= */
export function createTableFilter(config) {
    const {
        inputs,
        rows,
        getRowData,
        matchRow
    } = config;

    const inputList = Array.isArray(inputs)
        ? inputs
        : Object.values(inputs);

    function apply() {
        for (const row of rows) {
            const data = getRowData(row);
            row.style.display = matchRow(data) ? "" : "none";
        }
    }

    function bind() {
        for (const input of inputList) {
            const event = input.tagName === "SELECT" ? "change" : "input";
            input.addEventListener(event, apply);
        }
    }

    bind();
    apply();

    return { apply };
}

/* =========================
    MODALS
========================= */
export function createModal(modalId, config = {}) {
    const modal = document.getElementById(modalId);
    if (!modal) return null;

    const {
        closeOnOverlayClick = true,
        closeOnEsc = true
    } = config;

    function open() {
        modal.classList.remove("hidden");
        document.body.classList.add("modal-open");
    }

    function close() {
        modal.classList.add("hidden");
        document.body.classList.remove("modal-open");
    }

    function toggle() {
        const isHidden = modal.classList.contains("hidden");
        isHidden ? open() : close();
    }

    function bind() {
        modal.querySelectorAll(".btn-close-modal").forEach(btn => {
            btn.addEventListener("click", close);
        });

        if (closeOnOverlayClick) {
            modal.addEventListener("click", (e) => {
                if (e.target === modal) close();
            });
        }

        if (closeOnEsc) {
            document.addEventListener("keydown", (e) => {
                if (e.key === "Escape") close();
            });
        }
    }

    bind();

    return {
        open,
        close,
        toggle,
        element: modal
    };
}
