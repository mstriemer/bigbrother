xtag.register('x-data-list', {
    lifecycle: {
        created: function () {
            this.rootElement = this.children[0];
            this.template = this.rootElement.innerHTML;
            this.clearData();
            $.get(this.src).done(this.loadData.bind(this));
        },
    },
    accessors: {
        src: {attribute: 'src'},
        root: {attribute: 'root'},
    },
    methods: {
        loadData: function (data) {
            var results = data[this.root];
            var content;
            results.forEach((function (result) {
                content = this.template;
                for (var attr in result) {
                    content = content.replace(
                        new RegExp("{" + attr + "}", 'g'), result[attr]);
                }
                this.rootElement.innerHTML += content;
            }).bind(this));
        },
        clearData: function () {
            this.children[0].innerHTML = '';
        },
    },
});

document.addEventListener('DOMComponentsLoaded', function () {
    var appBar = document.querySelector('x-appbar');
    var flipBox = document.querySelector('x-flipbox');
    var changeTo = document.querySelector('.gameshow-name');

    xtag.query(appBar, '.nav').forEach(function (nav) {
        nav.addEventListener('click', function () {
            flipBox.toggle();
        });
    });

    changeTo.addEventListener('change', function (e) {
        appBar.heading = changeTo.value;
    });
});
