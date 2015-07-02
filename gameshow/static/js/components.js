let $ = (selector) => document.querySelectorAll(selector);
$.one = (selector) => document.querySelector(selector);
$.on = (el, eventName, handler) => el.addEventListener(eventName, handler);
$.el = function(tagName, stuff, ...content) {
    let tag = document.createElement(tagName);
    if (stuff) {
        Object.keys(stuff).forEach((name) => {
            tag.setAttribute(name, stuff[name]);
        });
    }
    if (content) {
        content.forEach((el) => {
            if (el === undefined) {
                return;
            } else if (el.split) {
                tag.textContent = el;
            } else if (el.forEach) {
                el.forEach((e) => {
                    if (e.split) {
                        e = document.createTextNode(e);
                    }
                    tag.appendChild(e);
                });
            } else {
                tag.appendChild(el);
            }
        });
    }
    return tag;
};
$.fetch = function(url, params) {
    let csrfToken = $.one('meta[name=csrf-token]').content;
    let csrfHeader = $.one('meta[name=csrf-header]').content;
    params = params || {};
    params.credentials = 'include';
    if (!params.headers) {
        params.headers = {};
    }
    params.headers[csrfHeader] = csrfToken;
    return fetch(url, params);
};

let React = {
    createElement() {
        return $.el.apply(this, arguments);
    },
};

let gameshow = JSON.parse($.one('meta[name=gameshow-data]').content);

document.body.appendChild($.el('h1', {}, gameshow.name));
document.body.appendChild($.el('create-event', {'gameshow': JSON.stringify(gameshow)}));
document.body.appendChild($.el('event-list', {'gameshow': JSON.stringify(gameshow)}));

document.registerElement('create-event', class extends HTMLElement {
    createdCallback() {
        this.showCreateButton();
    }
    showCreateForm() {
        this.cleanup();
        let form = <form>
            <input name="gameshow" type="hidden" value={this.gameshow.pk} />
            <input name="name" placeholder="Event name" type="text" required />
            <input name="date" placeholder="Date aired" type="text" required />
            <input name="date_performed" placeholder="Date performed" type="text" required />
            <button type="submit">Create</button>
        </form>;
        $.on(form, 'submit', (e) => {
            e.preventDefault();
            this.onSubmit(e);
        });
        this.appendChild(form);
        this.querySelector('[name=name]').focus();
    }
    showCreateButton() {
        this.cleanup();
        let form = <form><button type="submit">Create event</button></form>;
        this.appendChild(form);
        $.on(form, 'click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.showCreateForm();
        });
    }
    cleanup() {
        let form = this.querySelector('form');
        if (form) {
            this.removeChild(form);
        }
    }
    onSubmit(e) {
        let form = e.target;
        $.fetch('/api/events/', {
            method: 'post',
            body: new FormData(form),
        }).then((response) => {
            if (response.status === 201) {
                response.json().then((event) => {
                    this.showCreateButton();
                });
            } else {
                response.json().then((error) => {
                    this.innerHTML = '';
                    let errors = Object.keys(error).map((err) => {
                        return <li>{err + ': ' + error[err]}</li>;
                    });
                    this.appendChild(<ul>
                        {errors}
                    </ul>);
                });
            }
        });
    }
    get gameshow() {
        return JSON.parse(this.getAttribute('gameshow'));
    }
});
document.registerElement('event-list', class extends HTMLElement {
    createdCallback() {
        let loadingIndicator = <div class="loading">Loading...</div>;
        this.appendChild(loadingIndicator);
        $.fetch(`/api/events/?gameshow=${gameshow.pk}`).then((response) => {
            if (response.ok) {
                response.json().then((events) => {
                    this.removeChild(loadingIndicator);
                    this.showEvents(events);
                });
            } else {
                console.log('error fetching event list');
                this.textContent = "Error fetching event list";
            };
        });
    }
    showEvents(events) {
        let container = document.createDocumentFragment();
        events.forEach((event) => {
            container.appendChild(<div class="event">{`${event.name} - ${event.date_performed}`}</div>);
        });
        this.appendChild(container);
    }
    get gameshow() {
        return JSON.parse(this.getAttribute('gameshow'));
    }
});
