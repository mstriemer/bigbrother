document.addEventListener('DOMComponentsLoaded', function () {
    var appBar = document.querySelector('x-appbar');
    var gravatar = document.querySelector('x-gravatar');
    var changeTo = document.querySelector('.gameshow-name');
    changeTo.addEventListener('change', function (e) {
        gravatar.email = changeTo.value;
    });
});
