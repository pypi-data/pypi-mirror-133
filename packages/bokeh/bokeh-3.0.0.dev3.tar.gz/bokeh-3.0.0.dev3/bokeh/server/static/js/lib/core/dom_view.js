import { View } from "./view";
import { createElement, remove, empty, style } from "./dom";
import base_css from "../styles/base.css";
export class DOMView extends View {
    get children_el() {
        return this.shadow_el ?? this.el;
    }
    initialize() {
        super.initialize();
        this.el = this._createElement();
    }
    remove() {
        remove(this.el);
        super.remove();
    }
    css_classes() {
        return [];
    }
    styles() {
        return [];
    }
    render() { }
    renderTo(element) {
        element.appendChild(this.el);
        this.render();
        this._has_finished = true;
        this.notify_finished();
    }
    _createElement() {
        return createElement(this.constructor.tag_name, { class: this.css_classes() });
    }
}
DOMView.__name__ = "DOMView";
DOMView.tag_name = "div";
export class DOMComponentView extends DOMView {
    initialize() {
        super.initialize();
        this.shadow_el = this.el.attachShadow({ mode: "open" });
        this.stylesheet_el = style({}, ...this.styles());
        this.shadow_el.appendChild(this.stylesheet_el);
    }
    styles() {
        return [base_css];
    }
    empty() {
        empty(this.shadow_el);
        this.shadow_el.appendChild(this.stylesheet_el);
    }
}
DOMComponentView.__name__ = "DOMComponentView";
//# sourceMappingURL=dom_view.js.map