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
            if (el.split) {
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

document.body.appendChild($.el('create-event', {'gameshow': JSON.stringify(gameshow)}));

document.registerElement('create-event', class extends HTMLElement {
    createdCallback() {
        let form = <form>
            <h1>{this.gameshow.name}</h1>
            <input name="gameshow" type="hidden" value={this.gameshow.pk} />
            <input name="name" placeholder="Event name" type="text" required />
            <input name="date" placeholder="Date aired" type="text" required />
            <input name="date" placeholder="Date aired" type="text" required />
            <button type="submit">Create</button>
        </form>;
        $.on(form, 'submit', (e) => {
            e.preventDefault();
            this.onSubmit(e);
        });
        this.appendChild(form);
    }
    onSubmit(e) {
        let form = e.target;
        $.fetch('/api/events/', {
            method: 'post',
            body: new FormData(form),
        }).then((response) => {
            if (response.status === 201) {
                response.json().then((event) => {
                    this.textContent = event.id;
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
