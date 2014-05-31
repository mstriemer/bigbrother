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
