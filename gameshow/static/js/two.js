document.addEventListener('DOMComponentsLoaded', function () {
    var appBar = document.querySelector('x-appbar');
    var changeTo = document.querySelector('.gameshow-name');
    changeTo.addEventListener('change', function (e) {
        appBar.heading = changeTo.value;
    });
});
